from fastapi import Path, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from typing import Annotated


import schemas
from models import SongModel
from database import SessionDep


song_routers = APIRouter()

@song_routers.get("/songs/{song_id}", response_model=None, description="Get song by ID")
async def get_song(song_id: Annotated[int, Path(ge=1)], session: SessionDep)-> SongModel: 
    query = select(SongModel)
    query = query.where(SongModel.id == song_id)
    song = await session.execute(query)
    song = song.scalar_one_or_none()
    
    if song is None:
        raise HTTPException(status_code=404, detail="Song Not Found")

    return song

@song_routers.post("/songs/", description="Add new song")
async def add_song(data : schemas.NewSong, session: SessionDep):
    new_song = SongModel(
        name=data.name,
        words=" ".join(data.words)
    )
    session.add(new_song)
    await session.commit()
    return new_song.__dict__

@song_routers.delete("/songs/{song_id}", response_model=None, description="Delete song by ID")
async def delete_song(song_id: Annotated[int, Path(ge=1)], session: SessionDep)-> SongModel: 
    query = select(SongModel)
    query = query.where(SongModel.id == song_id)
    res = await session.execute(query)
    song = res.scalar_one_or_none()

    if song is None:
        raise HTTPException(status_code=404, detail="Song Not Found")
    
    deleted_song = song
    await session.delete(song)
    await session.commit()

    return deleted_song