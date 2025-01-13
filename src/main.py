import uvicorn
from fastapi import FastAPI

from src.api.endpoints import project
from src.config import get_settings


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(project.router, prefix="/v1", tags=["project"])
    return app


if __name__ == "__main__":
    settings = get_settings()

    uvicorn.run(
        f"{__name__}:{create_app.__name__}",
        host="0.0.0.0",
        port=settings.web_port,
        reload=settings.is_debug,
        server_header=False,
        factory=True,
    )
