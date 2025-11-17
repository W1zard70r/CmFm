
from fastapi import Path, APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from typing import Annotated

from app.song_module.schemas import Song, NewSong
from app.song_module.models import SongModel
from app.database import get_db

song_routers = APIRouter(tags=["songs"])

@song_routers.get("/{song_id}", response_model=Song)
async def get_song(
    song_id: Annotated[int, Path(ge=1)],
    session = Depends(get_db)
):
    song = await session.get(SongModel, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return Song.from_orm(song)

@song_routers.post("/", response_model=NewSong)
async def add_song(
    data: NewSong,
    session = Depends(get_db)
):
    new_song = SongModel(**data.dict())
    session.add(new_song)
    await session.commit()
    await session.refresh(new_song)
    return NewSong.from_orm(new_song)

@song_routers.delete("/{song_id}", response_model=Song)
async def delete_song(
    song_id: Annotated[int, Path(ge=1)],
    session = Depends(get_db)
):
    song = await session.get(SongModel, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    deleted_song = Song.from_orm(song)
    await session.delete(song)
    await session.commit()
    return deleted_song