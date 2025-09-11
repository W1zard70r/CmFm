from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    mail: Mapped[str | None] = mapped_column(String(100))

    login: Mapped[str] = mapped_column(index=True)
    hashed_password: Mapped[str] = mapped_column(String)


class SongModel(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    words: Mapped[str | None] = mapped_column(String)
