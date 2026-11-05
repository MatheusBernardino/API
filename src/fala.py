import asyncio
import os

import aiohttp
import edge_tts
from edge_tts.exceptions import EdgeTTSException


class TTSError(Exception):
  """Falha ao sintetizar a voz com o Edge TTS."""


def _remover_se_existir(caminho: str) -> None:
  try:
    os.remove(caminho)
  except FileNotFoundError:
    pass


async def tts(
    texto: str,
    caminho_saida: str,
    nome_voz: str = "pt-BR-AntonioNeural",
    taxa: str = "+0%",
) -> str:
  """Converte o texto fornecido em arquivo de áudio MP3.

  Levanta TTSError em falhas do serviço e nunca deixa um .mp3 vazio ou
  incompleto no disco.
  """
  communicate = edge_tts.Communicate(text=texto, voice=nome_voz, rate=taxa)
  try:
    await communicate.save(caminho_saida)
  except aiohttp.ClientResponseError as e:
    _remover_se_existir(caminho_saida)
    if e.status == 403:
      raise TTSError(
          "O serviço do Edge TTS recusou a requisição (403). Tente novamente"
          " mais tarde e atualize o edge-tts (pip install -U edge-tts)."
      ) from e
    raise TTSError(f"O serviço do Edge TTS respondeu com erro HTTP {e.status}.") from e
  except (EdgeTTSException, aiohttp.ClientError, asyncio.TimeoutError) as e:
    _remover_se_existir(caminho_saida)
    raise TTSError(f"Falha ao sintetizar a voz com o Edge TTS: {e}") from e
  except BaseException:
    # Ctrl+C ou cancelamento: também não deixa arquivo pela metade.
    _remover_se_existir(caminho_saida)
    raise

  if not os.path.exists(caminho_saida) or os.path.getsize(caminho_saida) == 0:
    _remover_se_existir(caminho_saida)
    raise TTSError("O Edge TTS não devolveu áudio para este texto.")
  return caminho_saida
