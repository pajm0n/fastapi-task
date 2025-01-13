from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base

from src.config import get_settings

settings = get_settings()
DATABASE_URL = f"postgresql+asyncpg://{settings.database.user}:{settings.database.password}@{settings.database.host}:{settings.database.port}/{settings.database.db}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
