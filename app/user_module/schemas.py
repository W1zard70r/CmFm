from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class UserBase(BaseModel):
    name: str
    mail: EmailStr | None
    login: str

    class Config:
        orm_mode = True
        from_attributes = True

class NewUser(UserBase):
    password: str
    
class User(UserBase):
    id: int
