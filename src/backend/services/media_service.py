import logging
from datetime import datetime, timezone
from fastapi import UploadFile, HTTPException, status, Request
from src.backend.services.permission_service import check_permission
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.backend.models.media_model import Media
from src.backend.repositories.media_repository import (
    save_media_db,
    delete_media_by_id,
    get_all_media,
    is_media_shared
)
from src.backend.storage.media_storage import save_file, delete_file
from src.backend.validators.media_validator import (
    validate_file_extension,
    validate_mime_type,
    get_video_duration
)

from src.backend.core.config import settings
from src.backend.core.timezone import convert_to_local_timezone
from src.backend.core.responses import json_response
from src.backend.core.messages import (
    MEDIA_NOT_FOUND,
    MEDIA_DELETE_SUCCESS,
    UPLOAD_ERROR_FILE_TOO_LARGE,
    UPLOAD_SUCCESS,
    ERROR_UNEXPECTED,
    UPLOAD_ERROR_GENERIC,
    NO_PERMISSION_MSG
)

logger = logging.getLogger(__name__)


async def _validate_file(file: UploadFile, max_size_bytes: int) -> str:
    """Valida tipo, extensão e tamanho do arquivo. Retorna tipo detectado."""
    detected_type = validate_mime_type(file)
    validate_file_extension(file.filename, detected_type)

    file_size = 0
    while chunk := await file.read(1024 * 1024):
        file_size += len(chunk)
        if file_size > max_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=UPLOAD_ERROR_FILE_TOO_LARGE.format(
                    filename=file.filename,
                    max_size_mb=settings.MAX_UPLOAD_SIZE_MB
                )
            )

    file.file.seek(0)
    return detected_type


async def _save_file_and_generate_metadata(file: UploadFile, media_type: str, order: int, slideshow_id: int | None) -> Media:
    """Salva o arquivo e retorna um objeto Media com metadados preenchidos."""
    file_path, file_hash = await save_file(file, media_type)

    duration = (
        await get_video_duration(file_path)
        if "video" in media_type
        else settings.CAROUSEL_MEDIA_DURATION
    )

    size_mb = round(file.file._file.tell() / (1024 * 1024), 2)

    return Media(
        filename=file.filename,
        filepath=file_path,
        file_hash=file_hash,
        type=media_type,
        size_mb=size_mb,
        duration=duration,
        uploaded_at=convert_to_local_timezone(datetime.now(timezone.utc)),
        slideshow_id=slideshow_id,
        order=order
    )


async def _process_upload(
    files: list[UploadFile],
    session: AsyncSession,
    slideshow_id: int | None = None
):
    """Processa o upload de arquivos, gerando metadados e salvando no banco."""
    max_size_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    results = {"success": [], "errors": []}

    last_order = 0
    if slideshow_id:
        result = await session.execute(
            select(Media.order)
            .where(Media.slideshow_id == slideshow_id)
            .order_by(Media.order.desc())
            .limit(1)
        )
        last_order = result.scalar_one_or_none() or 0

    for file in files:
        try:
            media_type = await _validate_file(file, max_size_bytes)
            last_order += 1
            media = await _save_file_and_generate_metadata(file, media_type, last_order, slideshow_id)
            await save_media_db(media, session)

            results["success"].append(file.filename)
            logger.info(f"Arquivo '{file.filename}' salvo com sucesso.")

        except HTTPException as e:
            results["errors"].append(str(e.detail))
            logger.warning(f"Erro ao enviar '{file.filename}': {e.detail}")

    return results


async def upload_to_slideshow(
    slideshow_id: int,
    request: Request,
    files: list[UploadFile],
    session: AsyncSession,
    user  
):
    """Função principal para upload de mídias de um slideshow via rota."""

    has_permission = await check_permission(user, "can_upload_media")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)

    try:
        result = await _process_upload(files, session, slideshow_id)
        success = result["success"]
        errors = result["errors"]

        # Cenário 1: tudo certo
        if success and not errors:
            return json_response(
                success=True,
                message=UPLOAD_SUCCESS,
                data=result,
                status_code=200
            )

        # Cenário 2: parcial
        if success and errors:
            return json_response(
                success=False,
                message="Alguns arquivos foram enviados, outros falharam.",
                data=result,
                status_code=207
            )

        # Cenário 3: tudo errado
        if not success and errors:
            return json_response(
                success=False,
                message="Nenhum arquivo foi enviado com sucesso.",
                data=result,
                status_code=400
            )

        return json_response(success=False, message=ERROR_UNEXPECTED, status_code=500)

    except Exception as e:
        logger.error(f"Erro inesperado ao fazer upload: {e}")
        return json_response(success=False, message=ERROR_UNEXPECTED, status_code=500)


async def delete_media(media_id: int, session: AsyncSession, user):
    """Remove uma mídia do banco de dados e do sistema de arquivos, se não for compartilhada."""

    has_permission = await check_permission(user, "can_delete_media")
    if not has_permission:
        return json_response(success=False, message=NO_PERMISSION_MSG, status_code=403)


    media, is_shared = await is_media_shared(media_id, session)

    if not media:
        raise HTTPException(status_code=404, detail=MEDIA_NOT_FOUND)

    if not is_shared:
        await delete_file(media.filepath)
        logger.info(f"Arquivo físico removido: {media.filepath}")
    else:
        logger.info(f"Arquivo compartilhado. Apenas removendo do banco: {media.filepath}")

    success = await delete_media_by_id(media_id, session)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_UNEXPECTED
        )

    logger.info(f"Mídia ID {media_id} removida com sucesso do banco.")
    return {"success": True, "message": MEDIA_DELETE_SUCCESS}