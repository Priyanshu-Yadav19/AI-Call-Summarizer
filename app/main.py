from fastapi import FastAPI, UploadFile, File
import os
import shutil
import tempfile

from app.stt_engine import AI4BharatSTT

app = FastAPI()

stt_engine = None


@app.on_event("startup")
def startup_event():
    global stt_engine
    stt_engine = AI4BharatSTT()


@app.get("/")
def root():
    return {"message": "AI Call Agent is running"}


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), language: str = "hi"):
    suffix = os.path.splitext(file.filename)[1] or ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        transcript = stt_engine.transcribe(temp_path, language=language)
        return {"transcript": transcript}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)