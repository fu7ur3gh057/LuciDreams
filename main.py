import uvicorn

from src.core.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "src.web.application:get_app",
        workers=settings.WORKERS_COUNT,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )


if __name__ == "__main__":
    main()
