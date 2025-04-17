from pydantic import BaseModel, Field, field_validator
import re
import unicodedata


class SlideshowCreateSchema(BaseModel):
    """
    Schema para criação de uma nova pasta (slideshow).
    """
    name: str | None = None
    title: str = Field(..., min_length=3, max_length=255)
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value and not value.isidentifier():
            raise ValueError("O nome (name) deve conter apenas letras, números e underscores, e não pode começar com número.")
        return value

    @staticmethod
    def generate_slug_from_title(title: str) -> str:
        """
        Gera um identificador (slug) do tipo 'pasta_rh' a partir do título da pasta.
        Remove acentos, símbolos e converte para minúsculas com underscore.
        """
        slug = unicodedata.normalize("NFKD", title)
        slug = slug.encode("ascii", "ignore").decode("utf-8")
        slug = re.sub(r"[^\w\s]", "", slug)
        slug = re.sub(r"\s+", "_", slug)
        return slug.lower()


class SlideshowUpdateSchema(BaseModel):
    """
    Schema para atualização de uma pasta (slideshow).
    """
    title: str = Field(..., min_length=3, max_length=255)
    description: str | None = None
