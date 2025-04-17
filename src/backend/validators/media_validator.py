import re
import time
import logging
import magic
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from moviepy import VideoFileClip

from src.backend.core.config import settings

logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """Remove caracteres perigosos do nome do arquivo."""
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)


def validate_file_extension(filename: str, detected_mime_type: str):
    """Valida se a extensão do arquivo é compatível com o tipo de mídia detectado."""
    ext = filename.rsplit(".", 1)[-1].lower()
    detected_category = settings.MIME_TYPE_MAP.get(detected_mime_type)

    if detected_category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo MIME '{detected_mime_type}' não permitido."
        )

    if ext not in settings.ALLOWED_MEDIA_TYPES.get(detected_category, []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensão '{ext}' não permitida para '{detected_mime_type}'."
        )

    if ext in settings.DANGEROUS_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A extensão '{ext}' não é permitida por segurança."
        )


def validate_mime_type(file: UploadFile) -> str:
    """Verifica o MIME Type real do arquivo usando 'python-magic'."""
    mime = magic.Magic(mime=True)
    actual_mime = mime.from_buffer(file.file.read(2048))
    file.file.seek(0)

    if actual_mime not in settings.MIME_TYPE_MAP:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo MIME '{actual_mime}' não permitido para '{file.filename}'."
        )

    return actual_mime


async def get_video_duration(file_path: str) -> int:
    """Calcula a duração real de um vídeo em segundos."""
    try:
        file_path = Path(settings.UPLOAD_DIR) / Path(file_path)
        if not file_path.exists():
            logger.error(f"Arquivo não encontrado: {file_path}")
            return 0

        time.sleep(1)

        logger.info(f"Obtendo duração do vídeo: {file_path}")
        with VideoFileClip(str(file_path)) as clip:
            duration = int(clip.duration)

        logger.info(f"Duração obtida: {duration} segundos")
        return duration

    except Exception as e:
        logger.error(f"Erro ao obter duração do vídeo '{file_path}': {e}")
        return 0
