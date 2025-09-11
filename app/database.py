from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated
from fastapi import Depends

from models import Base


engine = create_async_engine(
    url="sqlite+aiosqlite:///chordy.db", 
    connect_args={"autocommit":False}
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def session_maker():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(session_maker)]

async def db_setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

