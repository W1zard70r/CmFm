from fastapi import Path, APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import Annotated

from app.user_module.models import UserModel
from app.user_module.schemas import User, NewUser
from app.database import get_db

user_routers = APIRouter(tags=["users"])

@user_routers.get("/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(ge=1)],
    session = Depends(get_db)
):
    user = await session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User.from_orm(user)

@user_routers.post("/", response_model=User)
async def add_user(
    data: NewUser,
    session = Depends(get_db)
):
    new_user = UserModel(
        name=data.name,
        mail=data.mail,
        login=data.login,
        hashed_password=data.password + "_hashed"
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return User.from_orm(new_user)

@user_routers.delete("/{user_id}", response_model=User)
async def delete_user(
    user_id: Annotated[int, Path(ge=1)],
    session = Depends(get_db)
):
    user = await session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = User.from_orm(user)
    await session.delete(user)
    await session.commit()
    return deleted_user
