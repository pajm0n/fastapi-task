from datetime import date
from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.exceptions import ProjectDoesNotExists
from src.models import AreaOfInterest, Project


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_project(self, project_id: str) -> Project | None:
        query = (
            select(Project)
            .options(joinedload(Project.area_of_interest))
            .where(Project.id == project_id)
            .limit(1)
        )
        projects = await self.session.scalars(query)
        return projects.first()

    async def list_projects(
        self, offset: int | None = None, limit: int | None = None
    ) -> Sequence[Project]:
        query = select(Project).options(joinedload(Project.area_of_interest))

        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        projects = await self.session.scalars(query)
        return projects.all()

    async def delete(self, project_id: str) -> None:
        await self.session.execute(delete(Project).where(Project.id == project_id))

    def create_project(
        self,
        name: str,
        description: str,
        start_date: date,
        end_date: date,
        geojson_data: dict,
    ) -> Project:
        area_of_interest = AreaOfInterest(geojson_data=geojson_data)
        self.session.add(area_of_interest)

        new_project = Project(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            area_of_interest=area_of_interest,
        )
        self.session.add(new_project)
        return new_project

    async def commit(self) -> None:
        await self.session.commit()

    async def refresh(self, project: Project) -> None:
        await self.session.refresh(project)
