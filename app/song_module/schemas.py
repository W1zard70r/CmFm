from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, List, Tuple
from enum import Enum

class NewSong(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    words: Annotated[str | None, Field(max_length=10000)]
    
    class Config:
        orm_mode = True
        from_attributes = True
        
class Song(NewSong):
    id: Annotated[int, Field(ge=0)]