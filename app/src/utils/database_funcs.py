from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database import async_session_maker, async_engine, Base


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def create_tables():
    async with async_engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)