from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from fastapi import HTTPException

from app.user_module.models import UserModel
from app.user_module.schemas import User
from app.auth_module.schemas import RegisterRequest, LoginRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        a = pwd_context.hash(password)
        print(f'{a=}')
        return a
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    async def get_user_by_login(session: AsyncSession, login: str) -> UserModel | None:
        result = await session.execute(select(UserModel).where(UserModel.login == login))
        return result.scalars().first()
    
    @staticmethod
    async def register_user(session: AsyncSession, data: RegisterRequest) -> User:
        existing_user = await AuthService.get_user_by_login(session=session, login=data.login)
        if existing_user:
            raise HTTPException(status_code=400, detail="Login already registered")
        
        hashed_password = AuthService.get_password_hash(data.password)
        new_user = UserModel(
            name=data.name,
            mail=data.mail,
            login=data.login,
            hashed_password=hashed_password
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return User.from_orm(new_user)
    
    @staticmethod
    async def authenticate_user(session: AsyncSession, data: LoginRequest) -> UserModel:
        user = await AuthService.get_user_by_login(session=session, login=data.login)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not AuthService.verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        return user 