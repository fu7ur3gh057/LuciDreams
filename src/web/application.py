from fastapi import FastAPI, HTTPException
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.core.exceptions import DAOException, AppException
from src.web.api.router import api_router
from src.web.lifetime import lifespan


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    application = FastAPI(
        title="LuciDreams API",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Security-Policy"],
    )

    @application.exception_handler(AppException)
    async def custom_exception_handler(request, exc: DAOException):
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)

    # Main router for the API.
    application.include_router(router=api_router, prefix="/api")
    return application
