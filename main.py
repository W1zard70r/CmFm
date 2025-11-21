from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.database import create_tables
from app.user_module.routers import user_routers
from app.song_module.routers import song_routers
from app.auth_module.routers import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    await create_tables()
    # Startup complete and ready to serve requests
    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

@app.get("/")
async def home():
    return {"message": "Hello World"}

app.include_router(auth_router, prefix="/auth")
app.include_router(song_routers, prefix="/songs")
app.include_router(user_routers, prefix="/users")

