import requests


def download_pexels_video(
    termos_busca: str, caminho_saida: str, pexels_api_key: str
) -> dict | None:
  """Busca um vídeo vertical em HD no Pexels, salva localmente e retorna metadados para créditos."""
  url = f"https://api.pexels.com/videos/search?query={termos_busca}&per_page=1&orientation=portrait"
  headers = {"Authorization": pexels_api_key}

  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    dados = response.json()
    videos = dados.get("videos", [])
    if videos:
      video = videos[0]
      # Pega o primeiro link direto para download do MP4
      arquivos_video = video.get("video_files", [])
      if arquivos_video:
        url_video_arquivo = arquivos_video[0]["link"]
        bytes_video = requests.get(url_video_arquivo).content
        with open(caminho_saida, "wb") as f:
          f.write(bytes_video)

        usuario = video.get("user", {})
        return {
            "autor": usuario.get("name", "Desconhecido"),
            "perfil_autor": usuario.get("url", ""),
            "url_video": video.get("url", ""),
            "id_video": video.get("id", ""),
        }
  return None