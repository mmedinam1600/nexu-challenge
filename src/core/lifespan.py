import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from sqlalchemy import text

from core.config import settings
from core.constants import MIN_AVERAGE_PRICE
from core.database import database
from crud.brand import CRUDBrand
from crud.model import CRUDModel
from models.brand import VehicleBrandModel
from models.model import VehicleModelModel
from schemas.brand import VehicleBrandCreateSchema
from schemas.model import VehicleModelCreateSchema


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
    db = database.SessionLocal()

    try:
        brand_crud = CRUDBrand(VehicleBrandModel)
        model_crud = CRUDModel(VehicleModelModel)

        if db.query(VehicleBrandModel).first() is not None:
            logger.info("La base de datos ya ha sido poblada. Saltando el sembrado.")
            return

        models_file = settings.BASE_DIR / "seeds" / "models.json"
        if not models_file.exists():
            logger.warning(f"El archivo de semillas no se encontró en {models_file}")
            return

        with open(models_file, "r") as f:
            models_data = json.load(f)

        new_brands = set()
        new_models = []
        for model_item in models_data:
            brand_name = model_item["brand_name"]
            average_price = (
                None
                if model_item["average_price"] == 0
                else model_item["average_price"]
            )
            model_name = model_item["name"]

            vehicle_brand_create_schema = VehicleBrandCreateSchema(
                name=brand_name,
            )

            if vehicle_brand_create_schema not in new_brands:
                brand = brand_crud.create(db, brand=vehicle_brand_create_schema)
                new_brands.add(vehicle_brand_create_schema)
            else:
                brand = brand_crud.get_by_name(db, name=brand_name)
                if not brand:
                    logger.warning(
                        f"La marca '{brand_name}' no se encuentra en la base de datos, no se puede agregar el modelo."
                    )
                    continue

            if average_price is not None and average_price < MIN_AVERAGE_PRICE:
                logger.info(
                    f"El modelo {model_name} tiene un precio promedio de {average_price}, debido al caso de uso de el average > {MIN_AVERAGE_PRICE}, este se ignora."
                )
                continue
            new_models.append(
                VehicleModelCreateSchema(
                    brand_id=brand.id, name=model_name, average_price=average_price
                )
            )

        model_crud.bulk_insert(db, models_data=new_models)

        logger.info(f"Se insertaron {len(new_brands)} marcas.")
        logger.info(f"Se insertaron {len(new_models)} modelos.")
        logger.info("¡Población de la base de datos completada!")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager para la aplicación FastAPI.
    """
    logger.info("Iniciando la aplicación...")
    init_db()
    seed_db()
    yield
    logger.info("Deteniendo la aplicación...")
