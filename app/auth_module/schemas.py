from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class RegisterRequest(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    mail: EmailStr | None = None
    login: Annotated[str, Field(max_length=100)]
    password: Annotated[str, Field(min_length=1)]

class LoginRequest(BaseModel):
    login: Annotated[str, Field(max_length=100)]
    password: Annotated[str, Field(min_length=1)]

class AuthResponse(BaseModel):
    message: str
    login: Annotated[str, Field(max_length=100)]