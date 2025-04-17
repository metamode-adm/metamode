from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

# Regex global para senha forte
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$'

# Regex opcional para usernames (sem espaços, acentos, etc.)
USERNAME_REGEX = r'^[a-zA-Z0-9_.-]+$'


class UserBase(BaseModel):
    """Base para schemas de usuário com campos comuns."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    is_active: bool = True
    role: str = Field(..., examples=["user", "admin", "superadmin"])

    @field_validator("username")
    def validar_username(cls, value):
        if not re.match(USERNAME_REGEX, value):
            raise ValueError("Nome de usuário deve conter apenas letras, números, ponto, traço ou underline.")
        return value


class UserCreateSchema(UserBase):
    """Schema para criação de um novo usuário."""
    password: str = Field(..., min_length=8)

    @field_validator("password")
    def validar_senha_forte(cls, value):
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                "A senha deve ter pelo menos 8 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial (!@#$%^&*)"
            )
        return value


class UserUpdateSchema(BaseModel):
    """Schema para atualização de dados de um usuário existente."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr]
    password: Optional[str] = Field(None)
    is_active: Optional[bool]
    role: Optional[str] = Field(None, examples=["user", "admin", "superadmin"])

    @field_validator("username")
    def validar_username(cls, value):
        if value and not re.match(USERNAME_REGEX, value):
            raise ValueError("Nome de usuário deve conter apenas letras, números, ponto, traço ou underline.")
        return value

    @field_validator("password")
    def validar_senha_forte(cls, value):
        if not value:
            return value
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                "A senha deve ter pelo menos 8 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial (!@#$%^&*)"
            )
        return value


class UserReadSchema(BaseModel):
    """Schema para exibição/leitura dos dados de um usuário."""
    id: str
    username: str
    email: EmailStr
    is_active: bool
    role: str

    class Config:
        from_attributes = True


class UserUpdateProfileSchema(BaseModel):
    """Schema para atualização do perfil (nome de usuário e e-mail)."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr]

    @field_validator("username")
    def validar_username(cls, value):
        if value and not re.match(USERNAME_REGEX, value):
            raise ValueError("Nome de usuário deve conter apenas letras, números, ponto, traço ou underline.")
        return value


class UserUpdatePasswordSchema(BaseModel):
    """Schema para alteração de senha do usuário."""
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    def validar_senha_forte(cls, value):
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                "A senha deve ter pelo menos 8 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial (!@#$%^&*)"
            )
        return value
