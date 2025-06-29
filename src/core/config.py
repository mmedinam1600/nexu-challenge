import os
from dotenv import load_dotenv
from pydantic import PostgresDsn, BaseModel

load_dotenv()


class Settings(BaseModel):
    ENVIRONMENT: str = os.getenv(
        "ENVIRONMENT", "local"
    )  # LOCAL, DEVELOPMENT, STAGING, PRODUCTION
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "NEXU Challenge")

    POSTGRES_URI: PostgresDsn = PostgresDsn(
        os.getenv(
            f"{ENVIRONMENT}_POSTGRES_URI", "postgresql://user:password@db:5432/db"
        )
    )

    TIME_ZONE: str = os.getenv("TIME_ZONE", "America/Mexico_City")
    VERSION: str = os.getenv("VERSION", "1.0.0")


settings = Settings()
