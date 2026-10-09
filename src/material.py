import requests

PEXELS_SEARCH_URL = "https://api.pexels.com/videos/search"
# (conexão, leitura) em segundos; o download do vídeo pode demorar mais que a busca
TIMEOUT_BUSCA = (5, 15)
TIMEOUT_DOWNLOAD = (5, 60)


class PexelsError(Exception):
  """Falha ao falar com o Pexels (chave inválida, limite, rede ou timeout)."""


def _get(url: str, **kwargs) -> requests.Response:
  try:
    return requests.get(url, **kwargs)
  except requests.Timeout as e:
    raise PexelsError("Tempo esgotado ao falar com o Pexels. Tente novamente.") from e
  except requests.RequestException as e:
    raise PexelsError(f"Erro de rede ao falar com o Pexels: {e}") from e


def download_pexels_video(
    termos_busca: str, caminho_saida: str, pexels_api_key: str
) -> dict | None:
  """Busca um vídeo vertical em HD no Pexels, salva localmente e retorna metadados para créditos.

  Retorna None se a busca não encontrar vídeo. Levanta PexelsError em falhas
  de chave, limite de requisições, rede ou timeout.
  """
  response = _get(
      PEXELS_SEARCH_URL,
      params={"query": termos_busca, "per_page": 1, "orientation": "portrait"},
      headers={"Authorization": pexels_api_key},
      timeout=TIMEOUT_BUSCA,
  )

  if response.status_code in (401, 403):
    raise PexelsError("PEXELS_API_KEY inválida ou sem permissão. Confira o arquivo .env.")
  if response.status_code == 429:
    raise PexelsError(
        "Limite de requisições do Pexels atingido (200/hora). Aguarde e tente de novo."
    )
  if response.status_code != 200:
    raise PexelsError(f"Pexels respondeu com erro HTTP {response.status_code}.")

  try:
    videos = response.json().get("videos", [])
  except ValueError as e:
    raise PexelsError("Resposta inválida do Pexels (não é JSON).") from e

  if not videos:
    return None

  video = videos[0]
  # Pega o primeiro link direto para download do MP4
  arquivos_video = video.get("video_files", [])
  if not arquivos_video:
    return None

  download = _get(arquivos_video[0]["link"], timeout=TIMEOUT_DOWNLOAD)
  if download.status_code != 200:
    raise PexelsError(f"Falha ao baixar o vídeo (HTTP {download.status_code}).")
  with open(caminho_saida, "wb") as f:
    f.write(download.content)

  usuario = video.get("user", {})
  return {
      "autor": usuario.get("name", "Desconhecido"),
      "perfil_autor": usuario.get("url", ""),
      "url_video": video.get("url", ""),
      "id_video": video.get("id", ""),
  }
