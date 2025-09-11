from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from uuid import uuid4, UUID
from typing import Optional

from database import SessionDep
from models import UserModel
from schemas import User, NewUser, AuthentificationUser
from sessions import SessionData, backend, cookie, SessionDataDep


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_login(session: AsyncSession, login: str) -> Optional[UserModel]: 
    query = select(UserModel).where(UserModel.login == login)
    user = await session.execute(query)
    return user.scalars().first()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(entered_password, hashed_password) -> bool:
    return pwd_context.verify(entered_password, hashed_password)


async def authentificate_user(session: AsyncSession, login: str, password: str) -> UserModel:
    user = await get_user_by_login(session=session, login=login)
    if not user:
        raise HTTPException(status_code=404, detail="user with such login Not Found")
    elif not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Password doesn't match the login")    
    return user

async def user_registration(session: AsyncSession, new_user: NewUser):
    res = await get_user_by_login(session=session, login=new_user.login)
    if res is not None:
        raise HTTPException(status_code=400, detail="Login has already taken")
    hashed_password = get_password_hash(new_user.password)
    db_new_user = UserModel(
        name = new_user.name,
        mail = new_user.mail,
        login = new_user.login,
        hashed_password = hashed_password
    )

    session.add(db_new_user)
    await session.commit()
    await session.refresh(db_new_user)
    new_user = User(
        id=db_new_user.id,
        name=db_new_user.name,
        mail=db_new_user.mail,
        login=db_new_user.login,
    )
    return new_user


async def create_session(login: str, response: Response):
    session = uuid4()
    data = SessionData(login=login)
    await backend.create(session, data)
    cookie.attach_to_response(response, session)
    return {"message":f"session create for {login}"}


auth_router = APIRouter()

@auth_router.post("/register", response_model=User)# регистрация пользователя (создание записи в базе данных и сессии).
async def register(user_data: NewUser, session: SessionDep):
    new_user = await user_registration(session=session, new_user=user_data)
    response = Response()
    await create_session(user_data.login, response=response)
    return new_user

@auth_router.post("/login")# вход пользователя (проверка пароля и создание сессии).
async def login(auth_data: AuthentificationUser, response: Response, session: SessionDep):
    user = await authentificate_user(session=session, login=auth_data.login, password=auth_data.password)
    await create_session(login=user.login, response=response)
    login = auth_data.login
    return {"message": f"Logged in as {login}"}

@auth_router.get("/whoami")# получение информации о текущем пользователе (только для авторизованных).
async def whoami(session_data: SessionDataDep):
    return {"login": session_data.login}

@auth_router.delete("/logout")# выход (удаление сессии).
async def logout(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return {"message":"Logged out"}