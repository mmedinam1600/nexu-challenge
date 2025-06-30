from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.model import (
    VehicleModelSchema,
    VehicleModelUpdateSchema,
)
from services.model_service import ModelService


router = APIRouter(prefix="/models", tags=["Models"])


@router.get("/", response_model=List[VehicleModelSchema])
async def get_models(
    db: Session = Depends(get_db),
    greater: float | None = Query(
        None, description="Filtrar modelos con precio promedio mayor a este valor"
    ),
    lower: float | None = Query(
        None, description="Filtrar modelos con precio promedio menor a este valor"
    ),
):
    """Obtiene una lista de todos los modelos, con filtros opcionales por precio."""
    return ModelService.get_all_models_filtered(db, greater=greater, lower=lower)


@router.put("/{model_id}", response_model=VehicleModelSchema)
async def edit_model_price(
    model_id: int, model_schema: VehicleModelUpdateSchema, db: Session = Depends(get_db)
):
    """Actualiza el precio de un modelo específico."""
    return ModelService.update_model_price(db, model_id, model_schema)
