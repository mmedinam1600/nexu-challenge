import typing as t
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.brand import (
    VehicleBrandSchema,
    VehicleBrandCreateSchema,
    VehicleBrandWithAveragePriceSchema,
)
from schemas.model import (
    VehicleModelSummarySchema,
    VehicleModelCreateSchema,
    VehicleModelSchema,
)
from services.brand_service import BrandService


router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("/", response_model=t.List[VehicleBrandWithAveragePriceSchema])
async def get_brands(db: Session = Depends(get_db)):
    """Obtiene una lista de todas las marcas de vehículos con el precio promedio de sus modelos."""
    return BrandService.get_all_brands_with_average_price(db)


@router.post(
    "/", response_model=VehicleBrandSchema, status_code=status.HTTP_201_CREATED
)
async def create_brand(
    brand_in: VehicleBrandCreateSchema, db: Session = Depends(get_db)
):
    """Crea una nueva marca de vehículo."""
    return BrandService.create_brand(db, brand_in=brand_in)


@router.get("/{brand_id}/models", response_model=t.List[VehicleModelSummarySchema])
async def get_brand_models_by_id(brand_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los modelos de una marca específica."""
    return BrandService.get_brand_models_by_id(db, brand_id)


@router.post(
    "/{brand_id}/models",
    response_model=VehicleModelSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_brand_model(
    brand_id: int, model_in: VehicleModelCreateSchema, db: Session = Depends(get_db)
):
    """Crea un nuevo modelo para una marca específica."""
    return BrandService.create_brand_model(db, brand_id, model_in)
