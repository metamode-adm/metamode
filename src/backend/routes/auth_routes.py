from fastapi import APIRouter, Form, Request, Depends, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.core.database import get_db
from src.backend.core.templates import templates
from src.backend.core.responses import set_flash_message, get_flash_message
from src.backend.services.auth_service import authenticate_user, verificar_login
from src.backend.core.config import settings
from src.backend.core.messages import LOGIN_ERROR_INVALID_CREDENTIALS
from src.backend.models.user_model import User 
from src.backend.services.auth_service import get_current_user_with_permissions
import time

router = APIRouter()

@router.get("/")
async def root():
    return RedirectResponse(url="/login")

@router.get("/login")
async def login_page(request: Request):
    error = get_flash_message(request)
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    admin: bool = Form(False),
    session: AsyncSession = Depends(get_db),
):
    """
    Autentica o usuário e salva apenas o user_id na sessão.
    A validação de permissões será feita nas rotas via `check_permission`.
    """
    user = await authenticate_user(username, password, session)

    if not user:
        set_flash_message(request, LOGIN_ERROR_INVALID_CREDENTIALS)
        return RedirectResponse(url="/login", status_code=303)

    request.session["user_id"] = user.id
    if admin:
        request.session["expires"] = time.time() + settings.ADMIN_SESSION_EXPIRATION

    return RedirectResponse(url="/admin/media" if admin else "/carousel", status_code=303)

@router.get("/logout")
async def logout_redirect():
    return RedirectResponse(url="/login", status_code=303)

@router.post("/logout")
async def logout(request: Request, response: Response):
    request.session.clear()
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("session", httponly=True, secure=True, samesite="Strict")
    return response


@router.get("/no-permission")
async def no_permission(
    request: Request,
    
    user: User = Depends(get_current_user_with_permissions),
):
    flash_message = request.session.pop("flash_message", None)
    return templates.TemplateResponse("errors/no_permission.html", {
        "request": request,
        "flash_message": flash_message,
        "user": user, 
    })