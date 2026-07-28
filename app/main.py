import logging

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

@app.on_event("startup")
def startup_event() -> None:
    logger.info(
        "Starting %s in %s environment",
        settings.app_name,
        settings.app_env,
    )


@app.get("/", tags=["System"])
def root():
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@app.get("/health", tags=["System"])
def health():
    return {
        "status": "healthy",
        "service": settings.app_name,
    }


app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)