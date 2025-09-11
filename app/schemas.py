from pydantic import BaseModel
from typing import Annotated, List, Tuple
from enum import Enum


class Base(BaseModel):
    pass


class User(Base):
    id: Annotated[int]
    name: Annotated[str]
    email: Annotated[str]


class Chord(Enum):
    pass


# тут будут все возможные аккорды с https://tuneronline.ru/chords/

class Song(Base):
    id: Annotated[int]
    name: Annotated[str]
    words: Annotated[List[str]]

    isTABS: Annotated[bool]
    isCHORDS: Annotated[bool]

    Song_Chords: Annotated[List[Tuple[Chord, int]]]
    Song_Tabs: Annotated[List[Tuple[int]]]