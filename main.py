import asyncio
import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.database import create_tables
from app.user_module.routers import user_routers
from app.song_module.routers import song_routers
from app.auth_module.routers import auth_router

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

@app.get("/")
async def home():
    return {"message": "Hello World"}

app.include_router(auth_router, prefix="/auth")
app.include_router(song_routers, prefix="/songs")
app.include_router(user_routers, prefix="/users")

if __name__ == "__main__":
    asyncio.run(create_tables())
    uvicorn.run(app="main:app", host='127.0.0.1', port=8000, reload=True)
