from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_303_SEE_OTHER
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.exc import OperationalError
from src.backend.core.config import settings
from src.backend.routes import auth_routes, carrossel_routes, slideshow_routes, user_routes, user_profile_routes
from src.backend.core.templates import templates
import logging
from logging.handlers import RotatingFileHandler

# Garantindo que diretórios existam
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configurando nível do log
log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

# Handler para rotação de logs
log_file = settings.LOG_DIR / "app.log"
log_handler = RotatingFileHandler(
    log_file,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    "%Y-%m-%d %H:%M:%S"
)
log_handler.setFormatter(formatter)

logging.basicConfig(
    level=log_level,
    handlers=[log_handler, logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    # caso o ambiente de desenvolvimento esteja ativo, o modo debug do FastAPI será ativado.
    app = FastAPI(debug=settings.ENVIRONMENT == "development")

    # Static files
    app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

    # Middleware de segurança
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Ajuste em produção
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Ajuste em produção
    )

    # Middleware de sessão
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        same_site="Lax",
        https_only=False,  # True se HTTPS em produção
        max_age=settings.ADMIN_SESSION_EXPIRATION
    )

    # Registrar Rotas
    app.include_router(auth_routes.router)
    app.include_router(carrossel_routes.router)
    app.include_router(slideshow_routes.router)
    app.include_router(user_routes.router)
    app.include_router(user_profile_routes.router)

    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        if exc.status_code == HTTP_303_SEE_OTHER:
            return RedirectResponse(url=exc.headers["Location"], status_code=303)

        if exc.status_code in [401, 403]:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": exc.detail},
                status_code=exc.status_code
            )

        if exc.status_code == 404:
            context = {
                "request": request,
                "status_code": 404,
                "error_title": "Página não encontrada",
                "error_message": "A página que você está tentando acessar não existe."
            }
            return templates.TemplateResponse("errors/error.html", context, status_code=404)

        if exc.status_code == 500:
            context = {
                "request": request,
                "status_code": 500,
                "error_title": "Erro de conexão com o banco",
                "error_message": exc.detail or "Erro interno no servidor. Tente novamente mais tarde."
            }
            return templates.TemplateResponse("errors/error.html", context, status_code=500)

        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(StarletteHTTPException)
    async def custom_starlette_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            context = {
                "request": request,
                "status_code": 404,
                "error_title": "Página não encontrada",
                "error_message": "A página que você está tentando acessar não existe."
            }
            return templates.TemplateResponse("errors/error.html", context, status_code=404)

        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(OperationalError)
    async def db_exception_handler(request: Request, exc: OperationalError):
        logger.error(f"[DB ERROR] {exc}")
        return templates.TemplateResponse(
            "errors/error.html",
            {
                "request": request,
                "status_code": 500,
                "error_title": "Erro de banco de dados",
                "error_message": "Não foi possível acessar os dados no momento. Por favor, tente novamente mais tarde."
            },
            status_code=500
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"[UNHANDLED EXCEPTION] {repr(exc)}")
        return templates.TemplateResponse(
            "errors/error.html",
            {
                "request": request,
                "status_code": 500,
                "error_title": "Erro interno no servidor",
                "error_message": "Algo deu errado. Tente novamente mais tarde."
            },
            status_code=500
        )

    return app
