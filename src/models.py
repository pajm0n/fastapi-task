import uuid

from sqlalchemy import (Column, Date, DateTime, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import JSON

from src.infrastucture import db


class BaseModelMixin:
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created = Column(DateTime, server_default=func.now(), nullable=False)
    modified = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class AreaOfInterest(BaseModelMixin, db.Base):
    __tablename__ = "areas_of_interest"

    geojson_data = Column(JSON, nullable=False)
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )


class Project(BaseModelMixin, db.Base):
    __tablename__ = "projects"

    name = Column(String(32), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    area_of_interest = relationship(
        AreaOfInterest, backref="project", passive_deletes=True, uselist=False
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date_range": {"start": self.start_date, "end": self.end_date},
            "area_of_interest": (
                self.area_of_interest.geojson_data if self.area_of_interest else {}
            ),
        }
