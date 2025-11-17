from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from app.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    mail: Mapped[str | None] = mapped_column(String(100))

    login: Mapped[str] = mapped_column(index=True)
    hashed_password: Mapped[str] = mapped_column(String)