class ProjectDoesNotExists(Exception): ...


class GeoJSONParseException(Exception):
    def __init__(self, message: str = "", errors: list[str] | None = None) -> None:
        self.errors = errors if errors else []
        self.message = message
        super().__init__(self.message)
