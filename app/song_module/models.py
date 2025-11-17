from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.database import Base

class SongModel(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    words: Mapped[str | None] = mapped_column(String)