import typing as t
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.brand import VehicleBrandSchema, VehicleBrandCreateSchema
from crud.brand import CRUDBrand


router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("/", response_model=t.List[VehicleBrandSchema])
async def get_brands(db: Session = Depends(get_db)):
    """Obtiene una lista de todas las marcas de vehículos."""
    return CRUDBrand.get_all(db)


@router.post(
    "/", response_model=VehicleBrandSchema, status_code=status.HTTP_201_CREATED
)
async def create_brand(
    brand_in: VehicleBrandCreateSchema, db: Session = Depends(get_db)
):
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


@router.get("/:id/models")
async def get_brand_models_by_id(id: str) -> str:
    return f"Brand models: {id}"


@router.post("/:id/models")
async def create_brand_model(id: str) -> str:
    return f"Brand models: {id}"
