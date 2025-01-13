from datetime import date

from src.exceptions import ProjectDoesNotExists
from src.parsers import GeoJsonParser
from src.repositories import ProjectRepository


class ProjectService:
    def __init__(
        self, project_repository: ProjectRepository, geojson_parser: GeoJsonParser
    ) -> None:
        self.project_repository = project_repository
        self.geojson_parser = geojson_parser

    async def create(
        self,
        name: str,
        description: str,
        start_date: date,
        end_date: date,
        geojson_bytes: bytes,
    ) -> dict:
        geojson_data = self.geojson_parser.load(geojson_bytes)
        project = self.project_repository.create_project(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            geojson_data=geojson_data.model_dump(),
        )
        await self.project_repository.commit()
        return project.to_dict()

    async def get(self, project_id: str) -> dict:
        project = await self.project_repository.get_project(project_id)
        if not project:
            raise ProjectDoesNotExists()
        return project.to_dict()

    async def delete(self, project_id: str) -> None:
        project = await self.project_repository.get_project(project_id)
        if not project:
            raise ProjectDoesNotExists()
        await self.project_repository.delete(project_id=project_id)
        await self.project_repository.commit()

    async def list(self, page: int = 1, page_size: int = 10) -> tuple[list[dict], bool]:
        offset = (page - 1) * page_size
        projects = await self.project_repository.list_projects(offset, page_size + 1)
        has_next_page = len(projects) == page_size + 1

        return [project.to_dict() for project in projects[:page_size]], has_next_page

    async def update(
        self,
        project_id: str,
        name: str | None,
        description: str | None,
        start_date: date | None,
        end_date: date | None,
        geojson_bytes: bytes | None,
    ) -> dict:
        project = await self.project_repository.get_project(project_id)
        if not project:
            raise ProjectDoesNotExists()

        fields_to_update = {
            "name": name,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
        }

        for field, value in fields_to_update.items():
            if value is not None:
                setattr(project, field, value)

        if geojson_bytes is not None and project.area_of_interest:
            geojson_data = self.geojson_parser.load(geojson_bytes)
            project.area_of_interest.geojson_data = geojson_data.model_dump()

        await self.project_repository.commit()
        await self.project_repository.refresh(project)
        return project.to_dict()
