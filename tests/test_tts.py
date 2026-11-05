"""Testes das falhas do Edge TTS. Não usam internet."""
import asyncio

import aiohttp
import pytest
from edge_tts.exceptions import NoAudioReceived

import fala
import main


def _erro_http(status):
    return aiohttp.ClientResponseError(request_info=None, history=(), status=status)


def _comunicate_falso(monkeypatch, erro=None, conteudo=b"audio"):
    class Falso:
        def __init__(self, **kw):
            pass

        async def save(self, caminho):
            with open(caminho, "wb") as f:  # o edge-tts abre o arquivo antes de falar com o serviço
                if erro is None:
                    f.write(conteudo)
            if erro is not None:
                raise erro

    monkeypatch.setattr(fala.edge_tts, "Communicate", Falso)


def test_tts_403_vira_erro_claro_e_apaga_arquivo(monkeypatch, tmp_path):
    destino = tmp_path / "a.mp3"
    _comunicate_falso(monkeypatch, erro=_erro_http(403))

    with pytest.raises(fala.TTSError, match="403"):
        asyncio.run(fala.tts("oi", str(destino)))

    assert not destino.exists()


def test_tts_outro_erro_http(monkeypatch, tmp_path):
    destino = tmp_path / "a.mp3"
    _comunicate_falso(monkeypatch, erro=_erro_http(500))

    with pytest.raises(fala.TTSError, match="500"):
        asyncio.run(fala.tts("oi", str(destino)))

    assert not destino.exists()


def test_tts_sem_audio_apaga_arquivo(monkeypatch, tmp_path):
    destino = tmp_path / "a.mp3"
    _comunicate_falso(monkeypatch, erro=NoAudioReceived("sem audio"))

    with pytest.raises(fala.TTSError):
        asyncio.run(fala.tts("oi", str(destino)))

    assert not destino.exists()


def test_tts_arquivo_vazio_nao_e_aceito(monkeypatch, tmp_path):
    destino = tmp_path / "a.mp3"
    _comunicate_falso(monkeypatch, conteudo=b"")

    with pytest.raises(fala.TTSError, match="não devolveu áudio"):
        asyncio.run(fala.tts("oi", str(destino)))

    assert not destino.exists()


def test_tts_sucesso_mantem_arquivo(monkeypatch, tmp_path):
    destino = tmp_path / "a.mp3"
    _comunicate_falso(monkeypatch)

    assert asyncio.run(fala.tts("oi", str(destino))) == str(destino)
    assert destino.read_bytes() == b"audio"


def test_main_sai_com_erro_se_tts_falhar(monkeypatch, tmp_path):
    monkeypatch.setattr(main, "load_dotenv", lambda: None)
    monkeypatch.setenv("PEXELS_API_KEY", "p")
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    monkeypatch.setattr("builtins.input", lambda _: "tema")
    monkeypatch.setattr(main, "generate_script", lambda **kw: [{"script": "oi", "search_keyword": "a"}])

    async def tts_falha(**kw):
        raise main.TTSError("403")

    monkeypatch.setattr(main, "tts", tts_falha)
    monkeypatch.setattr(main, "BASE_TEMP_DIR", str(tmp_path))
    with pytest.raises(SystemExit) as e:
        asyncio.run(main.main())
    assert e.value.code == 1
