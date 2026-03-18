import os
import uuid
import subprocess
from pathlib import Path

import imageio_ffmpeg as ffmpeg
from fastapi import UploadFile

from app.config import settings


ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".flac",
    ".ogg",
    ".aac",
    ".mp4",
    ".mpeg",
    ".webm",
}


def ensure_upload_dir() -> None:
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


def validate_file_extension(filename: str) -> None:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {ext}. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )


async def save_upload_file(upload_file: UploadFile) -> str:
    ensure_upload_dir()

    validate_file_extension(upload_file.filename or "audio.wav")

    file_ext = Path(upload_file.filename or "audio.wav").suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_name)

    content = await upload_file.read()

    file_size_mb = len(content) / (1024 * 1024)
    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        raise ValueError(
            f"File too large: {file_size_mb:.2f} MB. Max allowed is {settings.MAX_FILE_SIZE_MB} MB."
        )

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path


def convert_to_wav(input_path: str) -> str:
    """
    Convert supported input files to mono 16kHz WAV for STT
    using the FFmpeg binary provided by imageio-ffmpeg.
    """
    input_path_obj = Path(input_path)
    output_path = str(input_path_obj.with_suffix("")) + "_converted.wav"

    try:
        ffmpeg_path = ffmpeg.get_ffmpeg_exe()
    except Exception as e:
        raise ValueError(
            "FFmpeg binary could not be loaded. Install it with: pip install imageio[ffmpeg]"
        ) from e

    command = [
        ffmpeg_path,
        "-y",
        "-i", input_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-f", "wav",
        output_path,
    ]

    try:
        subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise ValueError(
            f"Audio conversion failed: {e.stderr.strip() or 'Unknown FFmpeg error'}"
        ) from e

    if not os.path.exists(output_path):
        raise ValueError("Converted WAV file was not created.")

    return output_path