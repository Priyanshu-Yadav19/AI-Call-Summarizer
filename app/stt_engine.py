import numpy as np
import soundfile as sf
import librosa
import torch
from transformers import AutoModel


class AI4BharatSTT:
    def __init__(self) -> None:
        print("Loading AI4Bharat STT model...")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = AutoModel.from_pretrained(
            "ai4bharat/indic-conformer-600m-multilingual",
            trust_remote_code=True,
        )

        self.model.to(self.device)
        self.model.eval()

        print("AI4Bharat STT model loaded successfully.")

    def _load_audio(self, audio_path: str):
        audio, sr = sf.read(audio_path)

        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)

        audio = audio.astype(np.float32)

        target_sr = 16000
        if sr != target_sr:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)

        wav = torch.tensor(audio, dtype=torch.float32).unsqueeze(0)
        return wav.to(self.device)

    def transcribe(self, audio_path: str, language: str = "hi", decoder: str = "rnnt"):
        wav = self._load_audio(audio_path)

        with torch.inference_mode():
            result = self.model(wav, language, decoder)

        if isinstance(result, (list, tuple)) and len(result) > 0:
            transcript = result[0]
        else:
            transcript = result

        transcript = str(transcript).strip()

        if not transcript:
            transcript = "No speech detected."

        return transcript