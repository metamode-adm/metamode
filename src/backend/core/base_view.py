from fastapi import Request
from starlette.templating import _TemplateResponse
from src.backend.core.templates import templates
from src.backend.core.responses import get_flash_message

async def render_admin_template(
    request: Request,
    template_name: str,
    context: dict = None,
    user: dict = None,
    status_code: int = 200
) -> _TemplateResponse:
    """
    Renderiza templates administrativos, incluindo contexto padrão (user e flash_message).
    """
    context = context or {}
    context.update({
        "request": request,
        "user": user,
        "flash_message": get_flash_message(request)
    })
    return templates.TemplateResponse(template_name, context, status_code=status_code)
