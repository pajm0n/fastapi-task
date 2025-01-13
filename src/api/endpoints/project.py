from pathlib import Path
from typing import Annotated, Generic, Type, TypeVar

from fastapi import (APIRouter, Depends, File, Form, HTTPException, Query,
                     UploadFile, status)
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError

from src.api.deps import project_service
from src.api.schemas import Project, ProjectCreate, ProjectList, ProjectUpdate
from src.exceptions import GeoJSONParseException, ProjectDoesNotExists
from src.services import ProjectService

router = APIRouter()


T = TypeVar("T", bound=BaseModel)


class FormAsJson(Generic[T]):
    def __init__(self, class_: Type[T]) -> None:
        self.class_ = class_

    def __call__(
        self,
        data: str = Form(
            ...,
            description="JSON containing project data",
            examples=[
                {
                    "name": "name",
                    "date_range": {"start": "2024-12-10", "end": "2024-12-11"},
                }
            ],
        ),
    ) -> T:
        try:
            return self.class_.model_validate_json(data)
        except ValidationError as e:
            raise HTTPException(
                detail=jsonable_encoder(e.errors()),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


async def process_area_of_interest(area_of_interest: File) -> bytes:
        if area_of_interest.content_type != "application/json":
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only JSON files are allowed.",
            )
        geojson_data = await area_of_interest.read()
        return geojson_data


@router.post(
    "/project",
    description=Path("api_docs/create_project.md").read_text(),
    response_model=Project,
)
async def create_project(
    area_of_interest: UploadFile,
    data: ProjectCreate = Depends(FormAsJson(ProjectCreate)),
    project_service: ProjectService = Depends(project_service),
) -> dict:
    geojson_data = await process_area_of_interest(area_of_interest)

    try:
        project = await project_service.create(
            name=data.name,
            description=data.description,
            start_date=data.date_range.start,
            end_date=data.date_range.end,
            geojson_bytes=geojson_data,
        )
        return project
    except GeoJSONParseException as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "type": "geojson_parsing",
                    "msg": ex.message,
                    "ctx": {"error": ex.errors},
                }
            ],
        )


@router.patch(
    "/project/{project_id}",
    description=Path("api_docs/update_project.md").read_text(),
    response_model=Project,
)
async def update_project(
    project_id: str,
    area_of_interest: UploadFile | None | str = None,
    data: ProjectUpdate = Depends(FormAsJson(ProjectUpdate)),
    project_service: ProjectService = Depends(project_service),
) -> dict:
    if area_of_interest:
        try:
            geojson_data = await process_area_of_interest(area_of_interest)
        except AttributeError:
            geojson_data = area_of_interest.encode("utf-8", errors="ignore")
    else:
        geojson_data = None

    try:
        project = await project_service.update(
            project_id=project_id,
            name=data.name,
            description=data.description,
            start_date=data.date_range.start if data.date_range else None,
            end_date=data.date_range.end if data.date_range else None,
            geojson_bytes=geojson_data,
        )
        return project
    except ProjectDoesNotExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except GeoJSONParseException as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "type": "geojson_parsing",
                    "msg": ex.message,
                    "ctx": {"error": ex.errors},
                }
            ],
        )


@router.get("/project/{project_id}", response_model=Project)
async def get_project(
    project_id: str,
    project_service: ProjectService = Depends(project_service),
) -> dict:
    try:
        project = await project_service.get(project_id)
        return project
    except ProjectDoesNotExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/project/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    project_service: ProjectService = Depends(project_service),
) -> None:
    try:
        await project_service.delete(project_id)
    except ProjectDoesNotExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/project", response_model=ProjectList)
async def get_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=50),
    project_service: ProjectService = Depends(project_service),
) -> dict:
    projects, has_next_page = await project_service.list(page, page_size)
    return {"results": projects, "elements": len(projects), "has_next_page": has_next_page, "page_size": page_size, "page": page}
