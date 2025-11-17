from fastapi import APIRouter, Depends, Response
from uuid import UUID, uuid4

from app.database import SessionDep
from app.auth_module.schemas import RegisterRequest, LoginRequest, AuthResponse
from app.auth_module.service import AuthService
from app.auth_module.sessions import SessionData, SessionDataDep, backend, cookie
from app.auth_module.schemas import User

auth_router = APIRouter(tags=["auth"])

@auth_router.post("/register", response_model=User)
async def register(data: RegisterRequest, session: SessionDep, response: Response):
    # Register user
    user = await AuthService.register_user(session=session, data=data)
    # Create session
    session_id = UUID(str(uuid4()))
    session_data = SessionData(login=user.login)
    await backend.create(session_id, session_data)
    cookie.attach_to_response(response, session_id)

    return user

@auth_router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, session: SessionDep, response: Response):
    # Authenticate user
    user = await AuthService.authenticate_user(session=session, data=data)
    # Create session
    session_id = UUID(str(uuid4()))
    session_data = SessionData(login=user.login)
    await backend.create(session_id=session_id, model=session_data)
    cookie.attach_to_response(response, session_id)
    return AuthResponse(message="Login successful", login=user.login)

@auth_router.post("/logout")
async def logout(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return {"message": "Logout successful"}

@auth_router.get("/whoami")
async def whoami(session_data: SessionDataDep):
    return {"login": session_data.login}
