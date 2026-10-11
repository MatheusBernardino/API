import asyncio
import os
import re
import sys
from datetime import datetime
import logging

from dotenv import load_dotenv
from material import PexelsError, download_pexels_video
from video import ajusta_video_e_audio
from fala import tts
from gerador_roteiro import ChaveInvalidaError, generate_script

logging.getLogger("google_genai").setLevel(logging.ERROR)

# Diretório raiz do projeto (uma pasta acima de /src)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_TEMP_DIR = os.path.join(ROOT_DIR, "temp_media")


def salvar_creditos(creditos: list[dict], pasta_saida: str) -> str:
  """Gera um arquivo creditos.txt na pasta da execução com a devida atribuição dos criadores."""
  caminho_creditos = os.path.join(pasta_saida, "creditos.txt")
  agora = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

  linhas = [
      "=" * 60,
      "ATRIBUIÇÃO E CRÉDITOS DAS MÍDIAS (PEXELS)",
      "=" * 60,
      f"Data de geração: {agora}",
      "Plataforma: Pexels (https://www.pexels.com)",
      "Licença: Licença Pexels (Royalty-Free / Uso Gratuito)",
      "Termos da Licença: https://www.pexels.com/license/",
      "",
      "Abaixo estão os créditos dos criadores dos vídeos utilizados:",
      "-" * 60,
  ]

  for c in creditos:
    linhas.append(f"[Cena {c['cena']}] Busca: \"{c['keyword']}\"")
    linhas.append(f"  - Criador/Fotógrafo: {c['autor']}")
    if c.get("perfil_autor"):
      linhas.append(f"  - Perfil: {c['perfil_autor']}")
    if c.get("url_video"):
      linhas.append(f"  - Link do Vídeo: {c['url_video']}")
    linhas.append("")

  linhas.append("=" * 60)
  linhas.append(
      "Dica: Você pode copiar e colar estes créditos na descrição do seu vídeo no YouTube, TikTok ou Instagram."
  )
  linhas.append("=" * 60)

  with open(caminho_creditos, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas) + "\n")

  return caminho_creditos


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
  creditos = []

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
    info_midia = download_pexels_video(
        termos_busca=cena["search_keyword"],
        caminho_saida=arquivo_video,
        pexels_api_key=pexels_api_key,
    )

    if not info_midia:
      raise RuntimeError(
          f"Falha ao obter mídia para o termo '{cena['search_keyword']}'"
      )

    autor = info_midia.get("autor", "Desconhecido")
    print(f"      Criador no Pexels: {autor}")

    arquivos_cenas.append({"audio_path": arquivo_audio, "video_path": arquivo_video})
    creditos.append({
        "cena": i + 1,
        "keyword": cena["search_keyword"],
        "autor": autor,
        "perfil_autor": info_midia.get("perfil_autor", ""),
        "url_video": info_midia.get("url_video", ""),
    })

  # 3. Interpola e renderiza o arquivo final
  print("\n[Render] Montando e interpolando arquivos via FFmpeg...")
  ajusta_video_e_audio(arquivos_cenas, caminho_saida)
  print(f"[Sucesso] Vídeo final gerado em: {caminho_saida}")

  # 4. Salva arquivo com os créditos das mídias
  caminho_creditos = salvar_creditos(creditos, pasta_execucao)
  print(f"[Créditos] Arquivo de créditos gerado em: {caminho_creditos}")


async def main():
    load_dotenv()
    pexels_key = os.getenv("PEXELS_API_KEY")
    if not pexels_key:
        print("[Erro] PEXELS_API_KEY não encontrada no arquivo .env.")
        sys.exit(1)
    if not os.getenv("GEMINI_API_KEY"):
        print("[Erro] GEMINI_API_KEY não encontrada no arquivo .env.")
        sys.exit(1)
    tema = input("Digite o tema do vídeo (ou deixe em branco para o padrão): ").strip()
    if not tema:
        tema = "Curiosidades sobre o Universo"
    print(f"\n[1/3] Gerando roteiro com Gemini para: '{tema}'...")
    try:
        cenas = generate_script(video_subject=tema, paragraph_number=8)
    except ChaveInvalidaError as e:
        print(f"[Erro] {e}")
        sys.exit(1)
    if not cenas:
        print("[Erro] Não foi possível gerar o roteiro. Operação cancelada.")
        sys.exit(1)
    print(f"[Roteiro] {len(cenas)} cenas geradas com sucesso!")

    # Cria subpasta única para esta execução dentro de temp_media
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug_tema = re.sub(r"[^\w\s-]", "", tema).strip().lower().replace(" ", "_")[:25]
    nome_pasta = f"run_{timestamp}_{slug_tema}" if slug_tema else f"run_{timestamp}"
    pasta_execucao = os.path.join(BASE_TEMP_DIR, nome_pasta)

    caminho_saida = os.path.join(pasta_execucao, "video_final.mp4")

    print(f"\n[2/3] Iniciando produção do vídeo (temporários em: temp_media/{nome_pasta})...")
    try:
        await process_and_render_video(
            cenas_input=cenas,
            pexels_api_key=pexels_key,
            caminho_saida=caminho_saida,
            pasta_execucao=pasta_execucao,
        )
    except (PexelsError, RuntimeError) as e:
        print(f"[Erro] {e}")
        sys.exit(1)
    print(f"\n[3/3] Pipeline concluído! Abra o arquivo '{caminho_saida}' para assistir.")


if __name__ == "__main__":
    asyncio.run(main())

