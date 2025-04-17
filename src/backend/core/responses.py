from fastapi.responses import JSONResponse
from src.backend.core.templates import templates
from typing import Any
from starlette.requests import Request
from starlette.responses import Response


def render_login_error(request, templates, error_message):
    return templates.TemplateResponse("login.html", {"request": request, "error": error_message})


def redirect_to_carousel():
    return JSONResponse(
        status_code=303,
        headers={"Location": "/carousel"}
    )


def set_flash_message(request: Request, message: str):
    request.session["flash_message"] = message


def get_flash_message(request: Request):
    message = request.session.pop("flash_message", None)
    return message


def format_response(success: bool, message: str | None = None, data: Any = None):
    response = {"success": success}
    if message is not None:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return response


def json_response(success: bool, message: str | None = None, data: Any = None, status_code: int = None):
    return JSONResponse(
        content=format_response(success, message, data),
        status_code=status_code if status_code is not None else (200 if success else 400)
    )
