import os
import re
import json
import time
import logging
from dotenv import load_dotenv

logging.getLogger("google_genai").setLevel(logging.ERROR)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# ==============================================================================
# 1. CONSTANTES & LIMITES DE SEGURANÇA
# ==============================================================================
MIN_SCRIPT_PARAGRAPH_NUMBER = 1
MAX_SCRIPT_PARAGRAPH_NUMBER = 15
MAX_SCRIPT_PROMPT_LENGTH = 2000
MAX_SCRIPT_SYSTEM_PROMPT_LENGTH = 8000
DEFAULT_MODEL_NAME = "gemini-3.5-flash-lite"
MAX_RETRIES = 5

DEFAULT_SCRIPT_SYSTEM_PROMPT = """
# Role: Fast-Paced Video Script Generator (Shorts, Reels, TikTok)

## Goals:
Generate a dynamic, high-retention video script structured into sequential scenes.
The total duration of the video must be between 30 and 50 seconds (typically 7 to 10 short scenes).

## Constraints:
1. The script must be returned as a valid JSON array of objects representing each scene in chronological order.
2. Fast Pacing: Each scene must contain only 1 short, punchy sentence (around 10 to 16 words, taking about 3 to 5 seconds to be spoken). Never write long paragraphs.
3. Total Length: Ensure the number of scenes produces a complete, engaging story between 30 and 50 seconds total speaking time.
4. Get straight to the point: start directly with a compelling hook without greetings like "welcome" or "hello".
5. Plain text only: do NOT include markdown formatting, hashtags, asterisks, emojis or symbols in the script text.
6. Object structure: each object must have exactly two keys:
   - "script": the spoken text for that scene (must be in the specified language, default to Brazilian Portuguese / pt-BR).
   - "search_keyword": 2 to 3 concise English descriptive keywords to find high quality matching stock video on Pexels for that specific scene.
7. Do not include voiceover indicators like "Narrator:", "[Scene 1]" or similar.
8. Strictly return ONLY the raw JSON array.
""".strip()

# ==============================================================================
# 2. FUNÇÕES DE VALIDAÇÃO
# ==============================================================================
def _normalize_script_paragraph_number(paragraph_number: int | None) -> int:
    try:
        value = int(paragraph_number or MIN_SCRIPT_PARAGRAPH_NUMBER)
    except (TypeError, ValueError):
        value = MIN_SCRIPT_PARAGRAPH_NUMBER

    if value < MIN_SCRIPT_PARAGRAPH_NUMBER or value > MAX_SCRIPT_PARAGRAPH_NUMBER:
        return max(MIN_SCRIPT_PARAGRAPH_NUMBER, min(value, MAX_SCRIPT_PARAGRAPH_NUMBER))
    
    return value

def _limit_script_text(text: str | None, max_length: int, field_name: str) -> str:
    value = (text or "").strip()
    if len(value) <= max_length:
        return value
    return value[:max_length]

# ==============================================================================
# 3. CONSTRUTOR DE PROMPT
# ==============================================================================
def build_script_prompt(
    video_subject: str,
    language: str = "pt-BR",
    paragraph_number: int = 1,
    video_script_prompt: str = "",
    custom_system_prompt: str = "",
) -> str:
    paragraph_number = _normalize_script_paragraph_number(paragraph_number)
    video_script_prompt = _limit_script_text(video_script_prompt, MAX_SCRIPT_PROMPT_LENGTH, "video_script_prompt")
    custom_system_prompt = _limit_script_text(custom_system_prompt, MAX_SCRIPT_SYSTEM_PROMPT_LENGTH, "custom_system_prompt")

    prompt = custom_system_prompt or DEFAULT_SCRIPT_SYSTEM_PROMPT
    prompt += f"""
# Initialization:
- video subject: {video_subject}
- number of paragraphs: {paragraph_number}
""".rstrip()

    if language:
        prompt += f"\n- language: {language}"

    if video_script_prompt:
        prompt += f"""
# Additional User Requirements:
{video_script_prompt}
""".rstrip()

    return prompt

# ==============================================================================
# 4. COMUNICAÇÃO COM O GEMINI SDK
# ==============================================================================
class ChaveInvalidaError(Exception):
    """Chave do Gemini ausente, inválida ou sem permissão. Repetir não adianta."""


def _eh_erro_de_chave(erro: Exception) -> bool:
    codigo = getattr(erro, "code", None)
    return codigo in (401, 403) or (codigo == 400 and "api key" in str(erro).lower())


def _normalize_text_response(content, llm_provider: str = "gemini") -> str:
    if content is None:
        raise ValueError(f"[{llm_provider}] returned empty text content")
    if not isinstance(content, str):
        raise TypeError(f"[{llm_provider}] returned non-text content: {type(content)}")
    return content.strip()

def _call_gemini_api(prompt: str, api_key: str = "", model_name: str = DEFAULT_MODEL_NAME, base_url: str = "") -> str:
    from google import genai
    from google.genai import errors, types

    resolved_key = api_key or os.getenv("GEMINI_API_KEY", "")
    if not resolved_key:
        raise ChaveInvalidaError("GEMINI_API_KEY não encontrada. Confira o arquivo .env.")

    http_options = types.HttpOptions(base_url=base_url) if base_url else None
    
    generation_config = types.GenerateContentConfig(
        temperature=0.5,
        top_p=1,
        top_k=1,
        max_output_tokens=2048,
        response_mime_type="application/json",
    )

    try:
        with genai.Client(api_key=resolved_key, http_options=http_options) as client:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=generation_config,
            )
            return _normalize_text_response(response.text, "gemini")
    except errors.ClientError as e:
        if _eh_erro_de_chave(e):
            raise ChaveInvalidaError(
                "GEMINI_API_KEY inválida ou sem permissão. Confira o arquivo .env."
            ) from e
        raise

# ==============================================================================
# 5. SANITIZAÇÃO DE SAÍDA & ORQUESTRADOR
# ==============================================================================
def _clean_text_for_tts(texto: str) -> str:
    """Remove marcações visuais indesejadas que prejudicam a fala do TTS."""
    texto = texto.replace("*", "")
    texto = texto.replace("#", "")
    texto = re.sub(r"\[.*?\]", "", texto)
    texto = re.sub(r"\(.*?\)", "", texto)
    return texto.strip()

def generate_script(
    video_subject: str,
    language: str = "pt-BR",
    paragraph_number: int = 8,
    video_script_prompt: str = "",
    custom_system_prompt: str = "",
    api_key: str = "",
    model_name: str = DEFAULT_MODEL_NAME,
) -> list[dict]:
    paragraph_number = _normalize_script_paragraph_number(paragraph_number)
    
    prompt = build_script_prompt(
        video_subject=video_subject,
        language=language,
        paragraph_number=paragraph_number,
        video_script_prompt=video_script_prompt,
        custom_system_prompt=custom_system_prompt,
    )

    final_scenes = []
    for attempt in range(MAX_RETRIES):
        try:
            raw_response = _call_gemini_api(
                prompt=prompt,
                api_key=api_key,
                model_name=model_name
            )
            
            if raw_response:
                # Sanitização defensiva contra blocos markdown (```json ... ```)
                cleaned_response = raw_response.strip()
                if cleaned_response.startswith("```"):
                    cleaned_response = re.sub(r"^```(?:json)?\s*", "", cleaned_response, flags=re.IGNORECASE)
                    cleaned_response = re.sub(r"\s*```$", "", cleaned_response).strip()

                cenas = json.loads(cleaned_response)
                for cena in cenas:
                    cena["script"] = _clean_text_for_tts(cena.get("script", ""))
                    final_scenes.append(cena)
                break
        except ChaveInvalidaError:
            # Erro permanente: não adianta tentar de novo.
            raise
        except Exception as e:
            print(f"[Aviso] Tentativa {attempt + 1}/{MAX_RETRIES} falhou: {e}")
            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt
                print(f"[Aviso] Aguardando {wait_time}s antes de tentar novamente (exponential backoff)...")
                time.sleep(wait_time)
            
    return final_scenes

if __name__ == "__main__":
    # Execução interativa
    try:
        user_topic = input("Digite o tema do roteiro (ou deixe em branco para o teste padrão): ").strip()
        test_topic = user_topic if user_topic else "Por que o agachamento é o rei dos exercícios de perna?"
        
        print(f"\nGerando roteiro em JSON para: '{test_topic}' (duração estimada: 30 a 50s)...")
        script_scenes = generate_script(video_subject=test_topic, paragraph_number=8)
        print("\n--- Roteiro Gerado ---")
        print(json.dumps(script_scenes, indent=2, ensure_ascii=False))
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
