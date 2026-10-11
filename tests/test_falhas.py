"""Testes das falhas de chave/rede. Não usam internet nem chaves reais."""
import asyncio
from unittest.mock import MagicMock

import pytest
import requests
from google import genai
from google.genai import errors

import gerador_roteiro
import main
import material


def _resposta(status=200, json_data=None, content=b""):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = json_data if json_data is not None else {}
    r.content = content
    return r


# ---------- Gemini ----------

def _cliente_que_falha(erro):
    cliente = MagicMock()
    cliente.__enter__.return_value = cliente
    cliente.models.generate_content.side_effect = erro
    return cliente


def test_gemini_chave_invalida_para_na_primeira_tentativa(monkeypatch):
    cliente = _cliente_que_falha(errors.ClientError(401, {"error": {"message": "x"}}))
    monkeypatch.setattr(genai, "Client", lambda **kw: cliente)
    monkeypatch.setattr(gerador_roteiro.time, "sleep", lambda s: None)

    with pytest.raises(gerador_roteiro.ChaveInvalidaError):
        gerador_roteiro.generate_script("tema", api_key="chave-errada")

    assert cliente.models.generate_content.call_count == 1


def test_gemini_api_key_not_valid_400_tambem_e_chave_invalida(monkeypatch):
    erro = errors.ClientError(400, {"error": {"message": "API key not valid."}})
    cliente = _cliente_que_falha(erro)
    monkeypatch.setattr(genai, "Client", lambda **kw: cliente)

    with pytest.raises(gerador_roteiro.ChaveInvalidaError):
        gerador_roteiro.generate_script("tema", api_key="chave-errada")


def test_gemini_erro_temporario_continua_com_retentativas(monkeypatch):
    cliente = _cliente_que_falha(errors.ServerError(503, {"error": {"message": "x"}}))
    monkeypatch.setattr(genai, "Client", lambda **kw: cliente)
    monkeypatch.setattr(gerador_roteiro.time, "sleep", lambda s: None)

    assert gerador_roteiro.generate_script("tema", api_key="k") == []
    assert cliente.models.generate_content.call_count == gerador_roteiro.MAX_RETRIES


def test_gemini_sem_chave_levanta_erro(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(gerador_roteiro.ChaveInvalidaError):
        gerador_roteiro.generate_script("tema")


def test_limpeza_de_texto_para_tts():
    assert gerador_roteiro._clean_text_for_tts("**Olá** [cena 1] mundo (nota)#") == "Olá  mundo"


# ---------- Pexels ----------

def test_pexels_chave_invalida(monkeypatch, tmp_path):
    monkeypatch.setattr(material.requests, "get", lambda *a, **k: _resposta(401))
    with pytest.raises(material.PexelsError, match="PEXELS_API_KEY"):
        material.download_pexels_video("space", str(tmp_path / "v.mp4"), "errada")


def test_pexels_limite_de_requisicoes(monkeypatch, tmp_path):
    monkeypatch.setattr(material.requests, "get", lambda *a, **k: _resposta(429))
    with pytest.raises(material.PexelsError, match="Limite"):
        material.download_pexels_video("space", str(tmp_path / "v.mp4"), "k")


def test_pexels_timeout_vira_erro_claro(monkeypatch, tmp_path):
    def estoura(*a, **k):
        raise requests.Timeout()

    monkeypatch.setattr(material.requests, "get", estoura)
    with pytest.raises(material.PexelsError, match="Tempo esgotado"):
        material.download_pexels_video("space", str(tmp_path / "v.mp4"), "k")


def test_pexels_sempre_envia_timeout(monkeypatch, tmp_path):
    chamadas = []

    def falso(url, **kwargs):
        chamadas.append(kwargs)
        if "api.pexels.com" in url:
            return _resposta(200, {"videos": [{
                "video_files": [{"link": "https://x/v.mp4"}],
                "user": {"name": "Ana", "url": "https://p/ana"},
                "url": "https://p/v", "id": 1,
            }]})
        return _resposta(200, content=b"bytes")

    monkeypatch.setattr(material.requests, "get", falso)
    info = material.download_pexels_video("space", str(tmp_path / "v.mp4"), "k")

    assert info["autor"] == "Ana"
    assert (tmp_path / "v.mp4").read_bytes() == b"bytes"
    assert len(chamadas) == 2 and all("timeout" in c for c in chamadas)


def test_pexels_sem_resultados_retorna_none(monkeypatch, tmp_path):
    monkeypatch.setattr(material.requests, "get", lambda *a, **k: _resposta(200, {"videos": []}))
    assert material.download_pexels_video("zzz", str(tmp_path / "v.mp4"), "k") is None


# ---------- main: encerra com código != 0 ----------

def test_main_sai_com_erro_se_faltar_chave_pexels(monkeypatch):
    monkeypatch.setattr(main, "load_dotenv", lambda: None)
    monkeypatch.delenv("PEXELS_API_KEY", raising=False)
    with pytest.raises(SystemExit) as e:
        asyncio.run(main.main())
    assert e.value.code == 1


def test_main_sai_com_erro_se_chave_gemini_invalida(monkeypatch):
    monkeypatch.setattr(main, "load_dotenv", lambda: None)
    monkeypatch.setenv("PEXELS_API_KEY", "p")
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    monkeypatch.setattr("builtins.input", lambda _: "tema")

    def falha(**kw):
        raise main.ChaveInvalidaError("GEMINI_API_KEY inválida")

    monkeypatch.setattr(main, "generate_script", falha)
    with pytest.raises(SystemExit) as e:
        asyncio.run(main.main())
    assert e.value.code == 1


def test_main_sai_com_erro_se_pexels_falhar(monkeypatch, tmp_path):
    monkeypatch.setattr(main, "load_dotenv", lambda: None)
    monkeypatch.setenv("PEXELS_API_KEY", "p")
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    monkeypatch.setattr("builtins.input", lambda _: "tema")
    monkeypatch.setattr(main, "generate_script", lambda **kw: [{"script": "oi", "search_keyword": "a"}])

    async def tts_falso(**kw):
        return kw["caminho_saida"]

    def pexels_falha(**kw):
        raise main.PexelsError("chave inválida")

    monkeypatch.setattr(main, "tts", tts_falso)
    monkeypatch.setattr(main, "download_pexels_video", pexels_falha)
    monkeypatch.setattr(main, "BASE_TEMP_DIR", str(tmp_path))
    with pytest.raises(SystemExit) as e:
        asyncio.run(main.main())
    assert e.value.code == 1
