import google.generativeai as genai
from app.config import settings
from app.prompts import (
    SYSTEM_PROMPT_SUMMARY,
    SYSTEM_PROMPT_WHATSAPP,
    SYSTEM_PROMPT_EMAIL,
)


class LLMEngine:
    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing in .env")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def _generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        text = getattr(response, "text", "") or ""
        text = text.strip()

        if not text:
            raise ValueError("Empty response received from LLM.")

        return text

    def summarize(self, transcript: str) -> str:
        prompt = f"{SYSTEM_PROMPT_SUMMARY}\n\nTranscript:\n{transcript}"
        return self._generate(prompt)

    def draft_whatsapp(self, transcript: str) -> str:
        prompt = f"{SYSTEM_PROMPT_WHATSAPP}\n\nTranscript:\n{transcript}"
        return self._generate(prompt)

    def draft_email(self, transcript: str) -> str:
        prompt = f"{SYSTEM_PROMPT_EMAIL}\n\nTranscript:\n{transcript}"
        return self._generate(prompt)