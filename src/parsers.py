from json.decoder import JSONDecodeError
from typing import Literal

import geojson
from pydantic import BaseModel
from pydantic_core import ValidationError
from sqlalchemy import exc

from src.exceptions import GeoJSONParseException


class Geometry(BaseModel):
    type: Literal["MultiPolygon"]
    coordinates: list[list[list[tuple[float, float]]]]


class Feature(BaseModel):
    type: Literal["Feature"]
    geometry: Geometry


class GeoJsonParser:
    def load(self, data: bytes) -> Feature:
        try:
            geo_json = geojson.loads(data)
        except JSONDecodeError as ex:
            raise GeoJSONParseException(
                "The uploaded GeoJSON file could not be loaded correctly. Please check the file.",
                [str(ex)],
            ) from ex

        try:
            feature = Feature(**geo_json)
        except ValidationError as ex:
            raise GeoJSONParseException(
                "The GeoJSON file contains errors",
                [
                    error.get("msg", "")
                    for error in ex.errors(
                        include_url=False, include_context=False, include_input=False
                    )
                ],
            )

        if not geo_json.is_valid:
            raise GeoJSONParseException(
                "The GeoJSON file contains errors", geo_json.errors()
            )

        return feature
