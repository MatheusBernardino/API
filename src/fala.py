import asyncio
import edge_tts


async def tts(
    texto: str,
    caminho_saida: str,
    nome_voz: str = "pt-BR-AntonioNeural",
    taxa: str = "+0%",
) -> str:
  """Converte o texto fornecido em arquivo de áudio MP3."""
  communicate = edge_tts.Communicate(text=texto, voice=nome_voz, rate=taxa)
  await communicate.save(caminho_saida)
  return caminho_saida