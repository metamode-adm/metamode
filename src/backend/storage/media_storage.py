import os
import hashlib
from pathlib import Path
from fastapi import UploadFile
from src.backend.core.config import settings
from src.backend.validators.media_validator import sanitize_filename
import logging
import gc
import asyncio
logger = logging.getLogger(__name__)

def hash_filename(filename: str) -> str:
    """Gera um hash curto no nome do arquivo para evitar duplicidade."""
    name, ext = os.path.splitext(filename)
    hash_val = hashlib.md5(filename.encode()).hexdigest()[:8]
    return f"{name}_{hash_val}{ext}"

async def save_file(file: UploadFile, media_type: str) -> tuple[str, str]:
    """Salva um arquivo no disco baseado em hash do conteúdo e retorna (filepath, file_hash)."""
    filename = sanitize_filename(file.filename)
    detected_category = settings.MIME_TYPE_MAP.get(media_type, "outros")
    file_extension = filename.rsplit(".", 1)[-1].lower()

    # Lê conteúdo do arquivo para calcular hash
    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()
    hashed_filename = f"{file_hash[:16]}.{file_extension}"

    # Pasta de destino
    media_folder = settings.UPLOAD_DIR / detected_category / file_extension
    media_folder.mkdir(parents=True, exist_ok=True)
    file_path = media_folder / hashed_filename

    # Salvar somente se ainda não existir
    if not file_path.exists():
        with file_path.open("wb") as buffer:
            buffer.write(content)
        logger.info(f"Arquivo salvo em: {file_path}")
    else:
        logger.info(f"Arquivo duplicado detectado, usando existente: {file_path}")

    relative_path = f"{detected_category}/{file_extension}/{hashed_filename}"
    return relative_path, file_hash

async def delete_file(file_path: str):
    """Deleta um arquivo do disco, garantindo que ele existe."""
    try:
        absolute_path = settings.UPLOAD_DIR / Path(file_path)

        if absolute_path.exists():
            # Tenta liberar o arquivo (caso esteja em uso)
            gc.collect()
            await asyncio.sleep(0.1)  # dá tempo pro SO liberar o handle

            absolute_path.unlink()
            logger.info(f"Arquivo excluído: {absolute_path}")
        else:
            logger.warning(f"Arquivo não encontrado: {absolute_path}")

    except Exception as e:
        logger.error(f"Erro ao excluir arquivo '{file_path}': {e}")