from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.schemas import ProcessResponse
from app.utils import save_upload_file, ensure_upload_dir
from app.latency_tracker import LatencyTracker
from app.stt_engine import AI4BharatSTT
from app.llm_engine import LLMEngine


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

ensure_upload_dir()

stt_engine = AI4BharatSTT()
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
    }


@app.post("/process", response_model=ProcessResponse)
async def process_audio(
    file: UploadFile = File(...),
    output_type: str = Form(...),
):
    output_type = output_type.strip().lower()

    if output_type not in {"whatsapp", "email"}:
        raise HTTPException(status_code=400, detail="output_type must be 'whatsapp' or 'email'.")

    latency = LatencyTracker()

    try:
        latency.start("upload_save_latency")
        file_path = await save_upload_file(file)
        latency.end("upload_save_latency")

        latency.start("stt_latency")
        transcript = stt_engine.transcribe(file_path)
        latency.end("stt_latency")

        latency.start("summary_latency")
        summary = llm_engine.summarize(transcript)
        latency.end("summary_latency")

        latency.start("draft_latency")
        if output_type == "email":
            draft = llm_engine.draft_email(transcript)
        else:
            draft = llm_engine.draft_whatsapp(transcript)
        latency.end("draft_latency")

        return ProcessResponse(
            transcript=transcript,
            summary=summary,
            draft=draft,
            latency=latency.report(),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") from e


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )