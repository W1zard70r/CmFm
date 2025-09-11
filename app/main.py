import asyncio
import uvicorn
from fastapi import FastAPI

from database import db_setup
from users_routers import user_routers
from songs_routers import song_routers
from auth import auth_router

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Hello World"}

app.include_router(auth_router, prefix="/auth")
app.include_router(song_routers, prefix="/songs")
app.include_router(user_routers, prefix="/users")

if __name__ == "__main__":
    asyncio.run(db_setup())
    uvicorn.run(app="main:app", host='127.0.0.1', port=8000, reload=True)
