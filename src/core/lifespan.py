from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from sqlalchemy import text

from .database import database
from models.brand import VehicleBrandModel
from models.model import VehicleModelModel


def init_db() -> None:
    """
    Crear esquemas y tablas si no existen.
    """
    logger.info("Iniciando el proceso de inicialización de la base de datos...")

    # Necesario para registrar los modelos en los metadatos de SQLAlchemy.
    _ = VehicleBrandModel
    _ = VehicleModelModel

    try:
        with database.engine.connect() as connection:
            logger.info("Creando el esquema 'vehicle' si no existe...")
            connection.execute(text("CREATE SCHEMA IF NOT EXISTS vehicle"))
            connection.commit()
            logger.success("Esquema 'vehicle' verificado/creado correctamente.")

        logger.info("Creando las tablas de los modelos si no existen...")
        database.Base.metadata.create_all(bind=database.engine)
        logger.success("Tablas verificadas/creadas correctamente.")

    except Exception as e:
        logger.error(
            f"Error crítico durante la inicialización de la base de datos: {e}"
        )
        raise


def seed_db() -> None:
    """
    Poblar las tablas con datos de prueba.
    """
    logger.info("Poblando las tablas con datos de prueba...")
    try:
        with database.engine.connect() as connection:
            connection.execute(text("INSERT INTO vehicle.brands (name, average_price) VALUES ('Acura', 702109) ON CONFLICT (name) DO NOTHING"))
            connection.execute(text("INSERT INTO vehicle.brands (name, average_price) VALUES ('Audi', 630759) ON CONFLICT (name) DO NOTHING"))
            connection.execute(text("INSERT INTO vehicle.brands (name, average_price) VALUES ('Bentley', 3342575) ON CONFLICT (name) DO NOTHING"))
            connection.execute(text("INSERT INTO vehicle.brands (name, average_price) VALUES ('BMW', 858702) ON CONFLICT (name) DO NOTHING"))
            connection.execute(text("INSERT INTO vehicle.brands (name, average_price) VALUES ('Buick', 290371) ON CONFLICT (name) DO NOTHING"))
            connection.commit()
    except Exception as e:
        logger.error(f"Error al poblar la tabla de marcas con datos de prueba: {e}")
        raise

    try:
        with database.engine.connect() as connection:
            connection.execute(text("INSERT INTO vehicle.models (name, average_price) VALUES ('ILX', 303176) ON CONFLICT (name) DO NOTHING"))
            connection.execute(text("INSERT INTO vehicle.models (name, average_price) VALUES ('MDX', 448193) ON CONFLICT (name) DO NOTHING"))
            connection.execute(text("INSERT INTO vehicle.models (name, average_price) VALUES ('NSX', 3818225) ON CONFLICT (name) DO NOTHING"))
            connection.execute(text("INSERT INTO vehicle.models (name, average_price) VALUES ('RDX', 395753) ON CONFLICT (name) DO NOTHING"))
            connection.execute(text("INSERT INTO vehicle.models (name, average_price) VALUES ('RL', 239050) ON CONFLICT (name) DO NOTHING"))
            connection.commit()
    except Exception as e:
        logger.error(f"Error al poblar la tabla de modelos con datos de prueba: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    """
    Gestor de contexto para el ciclo de vida de la aplicación de FastAPI.
    """
    logger.info("Ejecutando eventos de arranque (startup)...")
    init_db()
    seed_db()

    yield

    logger.info("Ejecutando eventos de apagado (shutdown)...")
