import asyncio
import os
import re
from datetime import datetime
import logging

from dotenv import load_dotenv
from material import download_pexels_video
from video import ajusta_video_e_audio
from fala import tts
from gerador_roteiro import generate_script

logging.getLogger("google_genai").setLevel(logging.ERROR)

# Diretório raiz do projeto (uma pasta acima de /src)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_TEMP_DIR = os.path.join(ROOT_DIR, "temp_media")


async def process_and_render_video(
    cenas_input: list[dict],
    pexels_api_key: str,
    caminho_saida: str,
    pasta_execucao: str | None = None,
):
  """Função principal que orquestra a geração de áudio, download de imagem/vídeo
  e a interpolação via FFmpeg.
  """
  if not pasta_execucao:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_execucao = os.path.join(BASE_TEMP_DIR, f"run_{timestamp}")

  os.makedirs(pasta_execucao, exist_ok=True)
  arquivos_cenas = []

  for i, cena in enumerate(cenas_input):
    arquivo_audio = os.path.join(pasta_execucao, f"audio_{i}.mp3")
    arquivo_video = os.path.join(pasta_execucao, f"video_{i}.mp4")

    # 1. Gera áudio via Edge TTS
    print(f"[Cena {i+1}/{len(cenas_input)}] Sintetizando áudio...")
    await tts(texto=cena["script"], caminho_saida=arquivo_audio)

    # 2. Baixa vídeo de fundo via Pexels
    print(
        f"[Cena {i+1}/{len(cenas_input)}] Baixando mídia para a keyword:"
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
  print("\n[Render] Montando e interpolando arquivos via FFmpeg...")
  ajusta_video_e_audio(arquivos_cenas, caminho_saida)
  print(f"[Sucesso] Vídeo final gerado em: {caminho_saida}")


async def main():
    load_dotenv()
    pexels_key = os.getenv("PEXELS_API_KEY")
    if not pexels_key:
        print("[Erro] PEXELS_API_KEY não encontrada no arquivo .env.")
        return
    tema = input("Digite o tema do vídeo (ou deixe em branco para o padrão): ").strip()
    if not tema:
        tema = "Curiosidades sobre o Universo"
    print(f"\n[1/3] Gerando roteiro com Gemini para: '{tema}'...")
    cenas = generate_script(video_subject=tema, paragraph_number=8)
    if not cenas:
        print("[Erro] Não foi possível gerar o roteiro. Operação cancelada.")
        return
    print(f"[Roteiro] {len(cenas)} cenas geradas com sucesso!")

    # Cria subpasta única para esta execução dentro de temp_media
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug_tema = re.sub(r"[^\w\s-]", "", tema).strip().lower().replace(" ", "_")[:25]
    nome_pasta = f"run_{timestamp}_{slug_tema}" if slug_tema else f"run_{timestamp}"
    pasta_execucao = os.path.join(BASE_TEMP_DIR, nome_pasta)

    caminho_saida = os.path.join(pasta_execucao, "video_final.mp4")

    print(f"\n[2/3] Iniciando produção do vídeo (temporários em: temp_media/{nome_pasta})...")
    await process_and_render_video(
        cenas_input=cenas,
        pexels_api_key=pexels_key,
        caminho_saida=caminho_saida,
        pasta_execucao=pasta_execucao,
    )
    print(f"\n[3/3] Pipeline concluído! Abra o arquivo '{caminho_saida}' para assistir.")


if __name__ == "__main__":
    asyncio.run(main())

