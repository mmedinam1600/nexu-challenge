from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api import router
from core.lifespan import lifespan


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan
    )

    # Configuración de CORS para que se pueda hacer peticiones desde el frontend de cualquier origen
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router)
    return application


app = create_application()
