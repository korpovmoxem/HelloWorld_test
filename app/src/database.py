from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.testing.schema import mapped_column

from app.config import settings


DATABASE_URL = settings.get_database_url()
async_engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Hero(Base):
    __tablename__ = 'heroes'

    external_id: Mapped[int]
    name: Mapped[str]
    full_name: Mapped[str]
    intelligence: Mapped[int]
    strength: Mapped[int]
    speed: Mapped[int]
    power: Mapped[int]