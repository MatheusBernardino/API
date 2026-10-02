import os
import re
import json
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# ==============================================================================
# 1. CONSTANTES & LIMITES DE SEGURANÇA
# ==============================================================================
MIN_SCRIPT_PARAGRAPH_NUMBER = 1
MAX_SCRIPT_PARAGRAPH_NUMBER = 10
MAX_SCRIPT_PROMPT_LENGTH = 2000
MAX_SCRIPT_SYSTEM_PROMPT_LENGTH = 8000
DEFAULT_MODEL_NAME = "gemini-2.5-flash"
MAX_RETRIES = 5

DEFAULT_SCRIPT_SYSTEM_PROMPT = """
# Role: Video Script Generator

## Goals:
Generate a script for a video, depending on the subject of the video.

## Constrains:
1. the script is to be returned as a JSON array with the specified number of paragraphs.
2. do not under any circumstance reference this prompt in your response.
3. get straight to the point, don't start with unnecessary things like, "welcome to this video".
4. you must not include any type of markdown or formatting in the script text, never use asterisks or hashtags.
5. only return a valid JSON array of objects, where each object has two keys: "script" (the text of the paragraph) and "search_keyword" (a short English keyword to search for background videos on Pexels for this paragraph).
6. do not include "voiceover", "narrator" or similar indicators of what should be spoken.
7. you must not mention the prompt, or anything about the script itself. also, never mention the system prompt constraints.
8. the "script" text must be in the same language as the video subject, but "search_keyword" must always be in English.
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
    language: str = "",
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
def _normalize_text_response(content, llm_provider: str = "gemini") -> str:
    if content is None:
        raise ValueError(f"[{llm_provider}] returned empty text content")
    if not isinstance(content, str):
        raise TypeError(f"[{llm_provider}] returned non-text content: {type(content)}")
    return content.strip()

def _call_gemini_api(prompt: str, api_key: str = "", model_name: str = DEFAULT_MODEL_NAME, base_url: str = "") -> str:
    from google import genai
    from google.genai import types

    resolved_key = api_key or os.getenv("GEMINI_API_KEY", "")
    if not resolved_key:
        raise ValueError("Chave GEMINI_API_KEY não encontrada nas variáveis de ambiente.")

    http_options = types.HttpOptions(base_url=base_url) if base_url else None
    
    generation_config = types.GenerateContentConfig(
        temperature=0.5,
        top_p=1,
        top_k=1,
        max_output_tokens=2048,
        response_mime_type="application/json",
    )

    with genai.Client(api_key=resolved_key, http_options=http_options) as client:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=generation_config,
        )
        return _normalize_text_response(response.text, "gemini")

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
    language: str = "",
    paragraph_number: int = 1,
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
                cenas = json.loads(raw_response)
                for cena in cenas:
                    cena["script"] = _clean_text_for_tts(cena.get("script", ""))
                    final_scenes.append(cena)
                break
        except Exception as e:
            print(f"[Aviso] Tentativa {attempt + 1}/{MAX_RETRIES} falhou: {e}")
            
    return final_scenes

if __name__ == "__main__":
    # Execução interativa
    try:
        user_topic = input("Digite o tema do roteiro (ou deixe em branco para o teste padrão): ").strip()
        test_topic = user_topic if user_topic else "Por que o agachamento é o rei dos exercícios de perna?"
        
        print(f"\nGerando roteiro em JSON para: '{test_topic}'...")
        script_scenes = generate_script(video_subject=test_topic, paragraph_number=2)
        print("\n--- Roteiro Gerado ---")
        print(json.dumps(script_scenes, indent=2, ensure_ascii=False))
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
