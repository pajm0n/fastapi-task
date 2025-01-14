from fastapi import FastAPI

from src.api.endpoints import project


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(project.router, prefix="/v1", tags=["project"])
    return app
