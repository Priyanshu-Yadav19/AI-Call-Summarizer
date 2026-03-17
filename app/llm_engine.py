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
        try:
            response = self.model.generate_content(prompt)
            print("Gemini raw response:", response)

            text = getattr(response, "text", None)

            if not text:
                candidates = getattr(response, "candidates", None)
                if candidates:
                    try:
                        parts = candidates[0].content.parts
                        text = "".join(
                            part.text for part in parts if hasattr(part, "text") and part.text
                        )
                    except Exception:
                        text = None

            text = (text or "").strip()

            if not text:
                raise ValueError("Empty response received from Gemini.")

            return text

        except Exception as e:
            print("Gemini generation error:", str(e))
            raise

    def summarize(self, transcript: str) -> str:
        if not transcript or not transcript.strip():
            raise ValueError("Transcript is empty. Cannot generate summary.")
        prompt = f"{SYSTEM_PROMPT_SUMMARY}\n\nTranscript:\n{transcript}"
        return self._generate(prompt)

    def draft_whatsapp(self, transcript: str) -> str:
        if not transcript or not transcript.strip():
            raise ValueError("Transcript is empty. Cannot generate WhatsApp draft.")
        prompt = f"{SYSTEM_PROMPT_WHATSAPP}\n\nTranscript:\n{transcript}"
        return self._generate(prompt)

    def draft_email(self, transcript: str) -> str:
        if not transcript or not transcript.strip():
            raise ValueError("Transcript is empty. Cannot generate email draft.")
        prompt = f"{SYSTEM_PROMPT_EMAIL}\n\nTranscript:\n{transcript}"
        return self._generate(prompt)