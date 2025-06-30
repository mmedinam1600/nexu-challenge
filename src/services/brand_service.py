import typing as t
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from crud.brand import CRUDBrand
from crud.model import CRUDModel
from schemas.brand import VehicleBrandCreateSchema, VehicleBrandWithAveragePriceSchema
from schemas.model import (
    VehicleModelSummarySchema,
    VehicleModelCreateSchema,
    VehicleModelCreateMigrationSchema,
)
from models.brand import VehicleBrandModel
from models.model import VehicleModelModel
from loguru import logger


class BrandService:
    @staticmethod
    def get_all_brands(db: Session) -> t.List[VehicleBrandModel]:
        """Obtiene una lista de todas las marcas de vehículos."""
        return CRUDBrand.get_all(db)

    @staticmethod
    def get_all_brands_with_average_price(
        db: Session,
    ) -> t.List[VehicleBrandWithAveragePriceSchema]:
        """Obtiene una lista de todas las marcas con el precio promedio de sus modelos."""
        result = (
            db.query(
                VehicleBrandModel.id,
                VehicleBrandModel.name,
                func.avg(VehicleModelModel.average_price).label("average_price"),
            )
            .outerjoin(
                VehicleModelModel, VehicleBrandModel.id == VehicleModelModel.brand_id
            )
            .filter(VehicleModelModel.average_price.isnot(None))
            .group_by(VehicleBrandModel.id, VehicleBrandModel.name)
            .all()
        )

        brands_with_avg_price = []
        for row in result:
            brands_with_avg_price.append(
                VehicleBrandWithAveragePriceSchema(
                    id=row.id, name=row.name, average_price=round(row.average_price)
                )
            )

        return brands_with_avg_price

    @staticmethod
    def get_brand_models_by_id(
        db: Session, brand_id: int
    ) -> t.List[VehicleModelSummarySchema]:
        """Obtiene todos los modelos de una marca específica."""
        # Verificar que la marca existe
        brand = CRUDBrand.get_by_id(db, brand_id)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La marca con id '{brand_id}' no existe.",
            )

        models = (
            db.query(
                VehicleModelModel.id,
                VehicleModelModel.name,
                VehicleModelModel.average_price,
            )
            .filter(VehicleModelModel.brand_id == brand_id)
            .all()
        )

        model_summaries = []
        for model in models:
            model_summaries.append(
                VehicleModelSummarySchema(
                    id=model.id, name=model.name, average_price=model.average_price
                )
            )

        return model_summaries

    @staticmethod
    def create_brand_model(
        db: Session, brand_id: int, model_schema: VehicleModelCreateSchema
    ) -> VehicleModelModel:
        """Crea un nuevo modelo para una marca específica."""
        brand = CRUDBrand.get_by_id(db, brand_id)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La marca con id '{brand_id}' no existe.",
            )

        existing_model = CRUDModel.get_by_name(db, name=model_schema.name)
        if existing_model:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El modelo '{model_schema.name}' ya existe.",
            )

        model_data = model_schema.model_dump()
        model_data["brand_id"] = brand_id
        logger.info(f"Model data: {model_data}")

        return CRUDModel.create(
            db, model=VehicleModelCreateMigrationSchema(**model_data)
        )

    @staticmethod
    def create_brand(
        db: Session, brand_in: VehicleBrandCreateSchema
    ) -> VehicleBrandModel:
        """
        Crea una nueva marca de vehículo.
        Valida que el nombre de la marca no exista.
        """
        existing_brand = CRUDBrand.get_by_name(db, name=brand_in.name)
        if existing_brand:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"La marca '{brand_in.name}' ya existe.",
            )
        return CRUDBrand.create(db, brand=brand_in)
