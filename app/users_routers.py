from fastapi import Path, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from typing import Annotated


import schemas
from models import UserModel
from database import SessionDep

user_routers = APIRouter()

@user_routers.get("/{user_id}", response_model=None, description="Get user by ID")
async def get_user(user_id: Annotated[int, Path(ge=1)], session: SessionDep)-> UserModel: 
    query = select(UserModel)
    query = query.where(UserModel.id == user_id)
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user

@user_routers.post("/", description="Add new user")
async def add_user(data : schemas.NewUser, session: SessionDep):
    new_user = UserModel(
        name=data.name,
        mail=data.mail,
        login=data.login,
        hashed_password=data.password + '***'
    )
    session.add(new_user)
    await session.commit()
    print("ok")
    return new_user.__dict__

@user_routers.delete("/{user_id}", response_model=None, description="Delete user by ID")
async def delete_user(user_id: Annotated[int, Path(ge=1)], session: SessionDep)-> UserModel: 
    query = select(UserModel)
    query = query.where(UserModel.id == user_id)
    res = await session.execute(query)
    user = res.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    deleted_user = user
    await session.delete(user)
    await session.commit()

    return deleted_user