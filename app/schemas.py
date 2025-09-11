from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, List, Tuple
from enum import Enum


class UserBase(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    mail: Annotated[EmailStr | None, Field(max_length=100)]
    login: Annotated[str, Field(max_length=100)]

class NewUser(UserBase):
    password: Annotated[str, str, Field(min_length=1)]
    
class User(UserBase):
    id: int

class AuthentificationUser(BaseModel):
    login: Annotated[str, Field(max_length=100)]
    password: Annotated[str, str, Field(min_length=1)]


class NewSong(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    words: Annotated[List[str] | None, Field(min_items=1)]

class Song(NewSong):
    id: Annotated[int, Field(ge=0)]
