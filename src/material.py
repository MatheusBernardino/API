import requests


def download_pexels_video(
    termos_busca: str, caminho_saida: str, pexels_api_key: str
) -> bool:
  """Busca um vídeo vertical em HD no Pexels e salva localmente."""
  url = f"https://api.pexels.com/videos/search?query={termos_busca}&per_page=1&orientation=portrait"
  headers = {"Authorization": pexels_api_key}

  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    dados = response.json()
    videos = dados.get("videos", [])
    if videos:
      # Pega o primeiro link direto para download do MP4
      arquivos_video = videos[0].get("video_files", [])
      if arquivos_video:
        url_video = arquivos_video[0]["link"]
        bytes_video = requests.get(url_video).content
        with open(caminho_saida, "wb") as f:
          f.write(bytes_video)
        return True
  return False