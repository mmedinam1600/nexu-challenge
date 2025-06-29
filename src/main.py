from fastapi import FastAPI
from core.config import settings
from api import router
from core.lifespan import lifespan


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan
    )
    application.include_router(router)
    return application


app = create_application()
