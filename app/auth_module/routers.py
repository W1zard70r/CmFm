from fastapi import APIRouter, Depends, Response
from uuid import UUID, uuid4

from app.database import get_db
from app.auth_module.schemas import RegisterRequest, LoginRequest, AuthResponse
from app.auth_module.service import AuthService
from app.auth_module.sessions import SessionData, SessionDataDep, backend, cookie
from app.user_module.schemas import User

auth_router = APIRouter(tags=["auth"])

@auth_router.post("/register", response_model=User)
async def register(data: RegisterRequest, response: Response, session = Depends(get_db)) -> User:
    # Register user
    user = await AuthService.register_user(session=session, data=data)
    # Create session
    session_id = UUID(str(uuid4()))
    session_data = SessionData(login=user.login)
    await backend.create(session_id, session_data)
    cookie.attach_to_response(response, session_id)

    return user

@auth_router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, response: Response, session = Depends(get_db)) -> AuthResponse:
    # Authenticate user
    user = await AuthService.authenticate_user(session=session, data=data)
    # Create session
    session_id = UUID(str(uuid4()))
    session_data = SessionData(login=user.login)
    await backend.create(session_id, session_data)
    cookie.attach_to_response(response, session_id)
    return AuthResponse(message="Login successful", login=user.login)

@auth_router.post("/logout", response_model=dict)
async def logout(response: Response, session_id: UUID | None = Depends(cookie)) -> dict:
    if not session_id:
        return {"message": "Not logged in"}
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return {"message": "Logout successful"}

@auth_router.get("/whoami", response_model=dict)
async def whoami(session_data: SessionDataDep) -> dict:
    print(session_data)
    if not session_data:
        return {"login": session_data.login}
    return {"login": None}
