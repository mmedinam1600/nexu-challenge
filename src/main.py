from fastapi import FastAPI
from core.config import settings
from api import router

app = FastAPI()


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    application.include_router(router)
    return application


app = create_application()
