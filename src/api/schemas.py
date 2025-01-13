from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from src.parsers import Feature


class DateRange(BaseModel):
    start: date
    end: date

    @field_validator("end")
    def check_start_before_end(cls, v: date, info: ValidationInfo) -> date:
        if "start" in info.data and v < info.data["start"]:
            raise ValueError("End date cannot be earlier than start date")
        return v


class ProjectCreate(BaseModel):
    name: Annotated[str, Field(max_length=32)]
    date_range: DateRange
    description: str = ""


class ProjectUpdate(BaseModel):
    name: Annotated[str | None, Field(max_length=32)] = None
    date_range: DateRange | None = None
    description: str | None = None


class Project(ProjectCreate):
    id: str
    area_of_interest: Feature


class ProjectList(BaseModel):
    results: list[Project]
    has_next_page: bool
    elements: int
    page_size: int
    page: int
