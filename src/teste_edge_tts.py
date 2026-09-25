import asyncio 
import edge_tts
TEXTO = "Olá! Este é um teste automatizado de síntese de voz usando Edge TTS."
VOZ = "pt-BR-AntonioNeural" 
ARQUIVO_SAIDA = "teste_audio.mp3"

async def testar_sintese_voz():
    print("Gerando áudio com Edge TTS...") 
    comunicador = edge_tts.Communicate(TEXTO, VOZ) 
    await comunicador.save(ARQUIVO_SAIDA) 
    print(f"Áudio gerado com sucesso: {ARQUIVO_SAIDA}")


if __name__ == "__main__": 
    asyncio.run(testar_sintese_voz())