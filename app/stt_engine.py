import os
from pathlib import Path

import nemo.collections.asr as nemo_asr
from huggingface_hub import login

from app.config import settings


class AI4BharatSTT:
    def __init__(self) -> None:
        print("Loading AI4Bharat STT model...")

        if settings.HF_TOKEN:
            login(token=settings.HF_TOKEN, add_to_git_credential=False)

        self.model = nemo_asr.models.ASRModel.from_pretrained(
            model_name="ai4bharat/indic-conformer-600m-multilingual"
        )

        print("AI4Bharat STT model loaded successfully.")

    def transcribe(self, audio_path: str) -> str:
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        results = self.model.transcribe([audio_path])
        transcript = results[0] if results else ""

        if isinstance(transcript, list):
            transcript = " ".join(map(str, transcript))

        transcript = str(transcript).strip()
        if not transcript:
            transcript = "No speech detected."

        return transcript