import asyncio
import os
from material import download_pexels_video
from video import ajusta_video_e_audio
from fala import tts


async def process_and_render_video(
    cenas_input: list[dict], pexels_api_key: str, caminho_saida: str
):
  """Função principal que orquestra a geração de áudio, download de imagem/vídeo

  e a interpolação via FFmpeg.
  """
  os.makedirs("temp_media", exist_ok=True)
  arquivos_cenas = []

  for i, cena in enumerate(cenas_input):
    arquivo_audio = f"temp_media/audio_{i}.mp3"
    arquivo_video = f"temp_media/video_{i}.mp4"

    # 1. Gera áudio via Edge TTS
    print(f"[Cena {i+1}] Sintetizando áudio...")
    await tts(texto=cena["script"], caminho_saida=arquivo_audio)

    # 2. Baixa vídeo de fundo via Pexels
    print(
        f"[Cena {i+1}] Baixando mídia para a keyword:"
        f" '{cena['search_keyword']}'..."
    )
    success = download_pexels_video(
        termos_busca=cena["search_keyword"],
        caminho_saida=arquivo_video,
        pexels_api_key=pexels_api_key,
    )

    if not success:
      raise RuntimeError(
          f"Falha ao obter mídia para o termo '{cena['search_keyword']}'"
      )

    arquivos_cenas.append({"audio_path": arquivo_audio, "video_path": arquivo_video})

  # 3. Interpola e renderiza o arquivo final
  print("[Render] Montando e interpolando arquivos via FFmpeg...")
  ajusta_video_e_audio(arquivos_cenas, caminho_saida)
  print(f"[Sucesso] Vídeo final gerado em: {caminho_saida}")

