# services/llm_service.py

from typing import Optional
import google.generativeai as genai
from config import GEMINI_API_KEY, LLM_MODEL_NAME, LLM_PROVIDER

# 🔹 Yeni: güvenli bir varsayılan model
DEFAULT_MODEL = "gemini-2.0-flash"

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. "
        "Create a .env file in the MediterraneoTropical folder and add GEMINI_API_KEY=..."
    )

genai.configure(api_key=GEMINI_API_KEY)


def call_llm(system_prompt: str, user_prompt: str, model: Optional[str] = None) -> str:
    model_name = model or LLM_MODEL_NAME or DEFAULT_MODEL

    if LLM_PROVIDER and LLM_PROVIDER.lower() not in ("gemini", "google", "google-gemini"):
        return (
            "LLM provider is not configured for Gemini. "
            "Set LLM_PROVIDER=gemini in your .env file to enable real responses."
        )

    try:
        gmodel = genai.GenerativeModel(model_name)
        response = gmodel.generate_content(
            [system_prompt, user_prompt],
        )

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        if getattr(response, "candidates", None):
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                return parts[0].text.strip()

        return "The LLM did not return any text content."

    except Exception as e:
        # Eğer 1.5-flash hatası alırsak otomatik 2.0-flash’e düş
        if "gemini-1.5-flash" in str(e):
            try:
                fallback_model = DEFAULT_MODEL
                gmodel = genai.GenerativeModel(fallback_model)
                response = gmodel.generate_content(
                    [system_prompt, user_prompt],
                )
                if hasattr(response, "text") and response.text:
                    return response.text.strip()
            except Exception as e2:
                return f"LLM ERROR (fallback {DEFAULT_MODEL}): {type(e2).__name__}: {e2}"

        return f"LLM ERROR: {type(e).__name__}: {e}"
