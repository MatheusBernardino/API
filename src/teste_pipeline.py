# Dados de teste para validação do pipeline (3 cenas / ~15 a 20 segundos de vídeo)
import asyncio
import os
from main import process_and_render_video
from dotenv import load_dotenv

dados_teste = [
    {
        "script": "No centro de muitas galáxias existe um buraco negro supermassivo devorando matéria.",
        "search_keyword": "galaxy space",
    },
    {
        "script": "A força gravitacional é tão intensa que nem mesmo a luz consegue escapar de seu horizonte de eventos.",
        "search_keyword": "black hole cosmos",
    },
    {
        "script": "O tempo ao redor dessas estruturas passa muito mais devagar para quem observa de fora.",
        "search_keyword": "universe stars space",
    },
]

load_dotenv()

PEXELS_KEY = os.getenv("PEXELS_API_KEY")

if __name__ == "__main__":
  print(">>> Iniciando teste do pipeline de renderização...")

  asyncio.run(
      process_and_render_video(
          cenas_input=dados_teste,
          pexels_api_key=PEXELS_KEY,
          caminho_saida="video_teste_resultado.mp4",
      )
  )

  print(">>> Teste finalizado! Verifique o arquivo 'video_teste_resultado.mp4'.")