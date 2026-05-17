import asyncio
import base64
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel

load_dotenv("../.env")

from app_agents.indigo_agent import BookingContext, init_vector_store, run_chat
from app_agents.interview_agent import init_resume_store, send_message, start_session

BASE_DIR = Path(__file__).parent
FAQ_PDF = BASE_DIR.parent / "openai_agents_sdk" / "docs" / "IndiGo_FAQ.pdf"
RESUME_PDF = BASE_DIR.parent / "openai_agents_sdk" / "docs" / "IshanDuttaResume.pdf"

_indigo_sessions: dict[str, dict] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    if FAQ_PDF.exists():
        print(f"Initializing IndiGo FAQ vector store from {FAQ_PDF}...")
        await init_vector_store(str(FAQ_PDF))
    else:
        print(f"Warning: IndiGo FAQ PDF not found at {FAQ_PDF}. Using keyword fallback.")

    if RESUME_PDF.exists():
        print(f"Initializing resume vector store from {RESUME_PDF}...")
        await init_resume_store(str(RESUME_PDF))
    else:
        print("Resume PDF not found. Interview agent will use web search only.")

    yield


app = FastAPI(title="Outskill Workshops Demo", lifespan=lifespan)

STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/{page}.html")
async def serve_page(page: str):
    file_path = STATIC_DIR / f"{page}.html"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(str(file_path))


# ---------- IndiGo Chat API ----------

class IndigoChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class IndigoChatResponse(BaseModel):
    reply: str
    agent: str
    handoffs: list[str]
    blocked: bool
    session_id: str


@app.post("/api/indigo/chat", response_model=IndigoChatResponse)
async def indigo_chat(req: IndigoChatRequest):
    session_id = req.session_id or "default"

    if session_id not in _indigo_sessions:
        _indigo_sessions[session_id] = {
            "history": [],
            "context": BookingContext(),
        }

    session = _indigo_sessions[session_id]

    result = await run_chat(
        user_message=req.message,
        history=session["history"],
        context=session["context"],
    )

    session["history"] = result["history"]
    session["context"] = result["context"]

    return IndigoChatResponse(
        reply=result["reply"],
        agent=result["agent"],
        handoffs=result["handoffs"],
        blocked=result["blocked"],
        session_id=session_id,
    )


# ---------- Interview API ----------

class InterviewStartResponse(BaseModel):
    session_id: str
    reply: str
    agent: str
    ended: bool


class InterviewMessageRequest(BaseModel):
    session_id: str
    message: str


class InterviewMessageResponse(BaseModel):
    reply: str
    agent: str
    handoffs: list[str]
    ended: bool


@app.post("/api/interview/start", response_model=InterviewStartResponse)
async def interview_start():
    result = await start_session()
    return InterviewStartResponse(
        session_id=result["session_id"],
        reply=result["reply"],
        agent=result["agent"],
        ended=result["ended"],
    )


@app.post("/api/interview/message", response_model=InterviewMessageResponse)
async def interview_message(req: InterviewMessageRequest):
    result = await send_message(req.session_id, req.message)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return InterviewMessageResponse(
        reply=result["reply"],
        agent=result["agent"],
        handoffs=result.get("handoffs", []),
        ended=result["ended"],
    )


# ---------- Voice Interview API ----------

_openai_client = OpenAI()


@app.post("/api/interview/voice")
async def interview_voice(
    session_id: str = Form(...),
    audio: UploadFile = File(...),
):
    audio_bytes = await audio.read()

    transcription = await asyncio.to_thread(
        lambda: _openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.webm", audio_bytes, audio.content_type or "audio/webm"),
        )
    )
    user_text = transcription.text.strip()

    if not user_text:
        raise HTTPException(status_code=400, detail="No speech detected")

    result = await send_message(session_id, user_text)

    tts_response = await asyncio.to_thread(
        lambda: _openai_client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=result["reply"],
            response_format="mp3",
        )
    )
    reply_audio_b64 = base64.b64encode(tts_response.content).decode()

    return {
        "user_transcript": user_text,
        "reply_text": result["reply"],
        "reply_audio": reply_audio_b64,
        "agent": result["agent"],
        "handoffs": result.get("handoffs", []),
        "ended": result["ended"],
    }


# ---------- TTS utility ----------

class TTSRequest(BaseModel):
    text: str
    voice: str = "nova"


@app.post("/api/tts")
async def tts(req: TTSRequest):
    tts_response = await asyncio.to_thread(
        lambda: _openai_client.audio.speech.create(
            model="tts-1",
            voice=req.voice,
            input=req.text,
            response_format="mp3",
        )
    )
    audio_b64 = base64.b64encode(tts_response.content).decode()
    return {"audio": audio_b64}
