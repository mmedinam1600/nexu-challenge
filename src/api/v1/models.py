import typing as t
from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session

from core.constants import MIN_AVERAGE_PRICE
from core.database import get_db
from schemas.model import (
    VehicleModelSchema,
    VehicleModelUpdateSchema,
    VehicleModelCreateSchema,
)
from crud.model import CRUDModel
from crud.brand import CRUDBrand
from models.model import VehicleModelModel


router = APIRouter(prefix="/models", tags=["Models"])


@router.get("/", response_model=t.List[VehicleModelSchema])
async def get_models(
    db: Session = Depends(get_db),
    greater: t.Optional[float] = Query(
        None, description="Filtrar modelos con precio promedio mayor a este valor"
    ),
    lower: t.Optional[float] = Query(
        None, description="Filtrar modelos con precio promedio menor a este valor"
    ),
):
    """
    Obtiene una lista de todos los modelos, con filtros opcionales por precio.
    """
    return CRUDModel.get_all_filtered(db, greater=greater, lower=lower)


@router.put("/{model_id}", response_model=VehicleModelSchema)
async def edit_model_price(
    model_id: int, model_in: VehicleModelUpdateSchema, db: Session = Depends(get_db)
):
    """
    Actualiza el precio de un modelo específico.
    """
    db_model = CRUDModel.get_by_id(db, model_id=model_id)
    if not db_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El modelo con id '{model_id}' no existe.",
        )

    update_data = model_in.model_dump(exclude_unset=True)
    if (
        "average_price" in update_data
        and update_data["average_price"] <= MIN_AVERAGE_PRICE
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio promedio debe ser mayor a 100,000",
        )

    return CRUDModel.update(db, db_model=db_model, model_in=update_data)


@router.post(
    "/", response_model=VehicleModelSchema, status_code=status.HTTP_201_CREATED
)
async def create_new_model(
    model_in: VehicleModelCreateSchema,
    brand_id: int,
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo modelo para una marca específica.
    """
    brand = CRUDBrand.get_by_id(db, brand_id=brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La marca con id '{brand_id}' no existe.",
        )

    existing_model = CRUDModel.get_by_name(db, name=model_in.name)
    if existing_model:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El modelo '{model_in.name}' ya existe.",
        )

    model_data = model_in.model_dump()
    model_data["brand_id"] = brand_id

    db_model = VehicleModelModel(**model_data)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model
