# src/backend/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import ClassVar

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    SECRET_KEY: str 
    MAX_UPLOAD_SIZE_MB: int = 100
    DEFAULT_TIMEZONE: str = "America/Sao_Paulo"
    ADMIN_SESSION_EXPIRATION: int = 3600
    CAROUSEL_MEDIA_DURATION: int = 5
    LOG_LEVEL: str = "INFO"
    UPLOAD_DIR: Path = Path("uploads")
    LOG_DIR: Path = Path("logs")
    ENVIRONMENT: str = "production"  

    ALLOWED_MEDIA_TYPES: ClassVar[dict] = {
        "image": ["jpg", "jpeg", "png", "webp"],
        "video": ["mp4", "webm"],
        "gif": ["gif"]
    }

    MIME_TYPE_MAP: ClassVar[dict] = {
        "image/jpeg": "image",
        "image/png": "image",
        "image/webp": "image",
        "image/gif": "gif",
        "video/mp4": "video",
        "video/webm": "video"
    }

    DANGEROUS_EXTENSIONS: ClassVar[list] = ["php", "exe", "sh", "bat", "py", "js", "html"]

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def DATABASE_URL(self):
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
