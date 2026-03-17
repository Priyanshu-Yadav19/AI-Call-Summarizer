from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import traceback

from app.config import settings
from app.schemas import ProcessResponse
from app.utils import save_upload_file, ensure_upload_dir
from app.latency_tracker import LatencyTracker
from app.stt_engine import SarvamSTT
from app.llm_engine import LLMEngine


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

ensure_upload_dir()

stt_engine = SarvamSTT()
llm_engine = LLMEngine()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "stt_provider": "sarvam",
        "stt_model": settings.SARVAM_MODEL,
    }


@app.post("/process", response_model=ProcessResponse)
async def process_audio(
    file: UploadFile = File(...),
    output_type: str = Form(...),
):
    output_type = output_type.strip().lower()

    if output_type not in {"whatsapp", "email"}:
        raise HTTPException(
            status_code=400,
            detail="output_type must be 'whatsapp' or 'email'."
        )

    latency = LatencyTracker()

    try:
        print("\n===== NEW REQUEST STARTED =====")
        print(f"Uploaded filename: {file.filename}")
        print(f"Requested output_type: {output_type}")

        latency.start("upload_save_latency")
        file_path = await save_upload_file(file)
        latency.end("upload_save_latency")
        print(f"File saved successfully: {file_path}")

        latency.start("stt_latency")
        transcript = stt_engine.transcribe(file_path)
        latency.end("stt_latency")
        print("STT completed successfully.")
        print(f"Transcript preview: {transcript[:300] if transcript else 'EMPTY'}")

        latency.start("summary_latency")
        summary = llm_engine.summarize(transcript)
        latency.end("summary_latency")
        print("Summary generated successfully.")
        print(f"Summary preview: {summary[:300] if summary else 'EMPTY'}")

        latency.start("draft_latency")
        if output_type == "email":
            draft = llm_engine.draft_email(transcript)
            print("Email draft generated successfully.")
        else:
            draft = llm_engine.draft_whatsapp(transcript)
            print("WhatsApp draft generated successfully.")
        latency.end("draft_latency")
        print(f"Draft preview: {draft[:300] if draft else 'EMPTY'}")

        response = ProcessResponse(
            transcript=transcript,
            summary=summary,
            draft=draft,
            latency=latency.report(),
        )

        print("ProcessResponse created successfully.")
        print("===== REQUEST COMPLETED =====\n")

        return response

    except ValueError as e:
        print("\n===== VALUE ERROR =====")
        traceback.print_exc()
        print("=======================\n")
        raise HTTPException(status_code=400, detail=str(e)) from e

    except FileNotFoundError as e:
        print("\n===== FILE NOT FOUND ERROR =====")
        traceback.print_exc()
        print("================================\n")
        raise HTTPException(status_code=404, detail=str(e)) from e

    except Exception as e:
        print("\n===== INTERNAL ERROR =====")
        traceback.print_exc()
        print("==========================\n")

        error_text = str(e)

        if "maximum limit of 30 seconds" in error_text or "Please use the batch API" in error_text:
            raise HTTPException(
                status_code=400,
                detail="This audio is longer than 30 seconds. Current Sarvam STT route supports only short audio. Use batch STT for long call recordings."
            ) from e

        raise HTTPException(status_code=500, detail=f"Internal error: {error_text}") from e


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )