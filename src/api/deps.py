from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.infrastucture import db
from src.parsers import GeoJsonParser
from src.repositories import ProjectRepository
from src.services import ProjectService


async def get_session() -> AsyncGenerator[db.AsyncSession, None]:
    async with db.async_session() as session:
        yield session


def project_service(session: AsyncSession = Depends(get_session)) -> ProjectService:
    return ProjectService(
        project_repository=ProjectRepository(session), geojson_parser=GeoJsonParser()
    )
