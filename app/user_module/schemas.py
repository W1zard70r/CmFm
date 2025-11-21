from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class UserBase(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    mail: EmailStr | None
    login: Annotated[str, Field(max_length=100)]

    class Config:
        orm_mode = True
        from_attributes = True

class NewUser(UserBase):
    password: Annotated[str, Field()]
    
class User(UserBase):
    id: int
