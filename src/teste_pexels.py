import os
import requests
import httpx
from dotenv import load_dotenv
load_dotenv() 
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def testar_busca_pexels_videos():
    if not PEXELS_API_KEY or PEXELS_API_KEY == "sua_chave_pexels_aqui":
        print(
            "Erro: Configure a PEXELS_API_KEY no arquivo .env antes de rodar o"
            "teste"
        )
        return

    # Fazendo a requisição para a API do Pexels para vídeos
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": "tecnologia", "per_page": 2, "orientation": "portrait"}
    print("Realizando requisição para API do Pexels...")
    try:
        response = httpx.get(url, headers=headers,params=params,timeout=10.0)
        response.raise_for_status()
        dados = response.json()
        total = dados.get("total_results", 0)
        print(f"Sucesso (status {response.status_code})!")
        print(f"Total de resultados encontrados: {total}\n")
        for video in dados.get("videos", []):
            files = video.get("video_files", [])
            if files:
                print(f"Vídeo ID {video['id']}: {files[0].get('link')}")
    except httpx.TimeoutException:
        print("A requisição excedeu o tempo limite (timeout).")
    except httpx.HTTPStatusError as e:
        print(f"Erro HTTP: {e.response.status_code}: Verifique se sua chave API"
            "está correta"
        )
    except Exception as e:
        print(f"Erro inesperado: {e}")


def testar_busca_pexels_imagem():
    if not PEXELS_API_KEY or PEXELS_API_KEY == "sua_chave_pexels_aqui":
        print(
            "Erro: Configure a PEXELS_API_KEY no arquivo .env antes de rodar o"
            "teste"
        )
        return

    # Fazendo a requisição para a API do Pexels para imagens
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": "tecnologia", "per_page": 4, "orientation": "portrait"}
    print("Realizando requisição para API do Pexels...")
    try:
        response = httpx.get(url, headers=headers,params=params,timeout=10.0)
        response.raise_for_status()
        dados = response.json()
        total = dados.get("total_results", 0)
        print(f"Sucesso (status {response.status_code})!")
        print(f"Total de resultados encontrados: {total}\n")
        for foto in dados.get("photos", []):
            # O dicionário 'src' traz as URLs da foto em vários tamanhos 
            src = foto.get("src", {}) 
            print(f"Foto ID {foto['id']} (Fotógrafo: {foto.get('photographer')}):") 
            print(f" - Original: {src.get('original')}")
            print(f" - Tamanho Médio: {src.get('medium')}\n")
    except httpx.TimeoutException:
        print("A requisição excedeu o tempo limite (timeout).")
    except httpx.HTTPStatusError as e:
        print(f"Erro HTTP: {e.response.status_code}: Verifique se sua chave API"
            "está correta"
        )
    except Exception as e:
        print(f"Erro inesperado: {e}")
if __name__ == "__main__":
    testar_busca_pexels_videos()
    testar_busca_pexels_imagem()
