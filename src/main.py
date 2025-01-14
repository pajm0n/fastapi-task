import uvicorn

from src.app import create_app
from src.config import get_settings

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
