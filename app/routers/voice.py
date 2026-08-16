from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends
from faster_whisper import WhisperModel
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)

UPLOAD_DIR = Path("uploads/audio")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_voice(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "Audio uploaded successfully",
        "path": str(file_path)
    }

model=WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

def transcribe_audio(file_path: str) -> str:
    segments, info = model.transcribe(file_path)

    text = " ".join(segment.text for segment in segments)

    return text.strip()