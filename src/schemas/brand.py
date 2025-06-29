from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID


class VehicleBrandBaseSchema(BaseModel):
    name: str
    average_price: Optional[Decimal] = Field(
        default=None,
        gt=100000,
        description="El precio promedio de la marca, debe ser mayor a 100,000",
    )


class VehicleBrandCreateSchema(VehicleBrandBaseSchema):
    pass


class VehicleBrandUpdateSchema(BaseModel):
    name: Optional[str] = None
    average_price: Optional[Decimal] = Field(
        default=None,
        gt=100000,
        description="El precio promedio de la marca, debe ser mayor a 100,000",
    )
    is_active: Optional[bool] = None


class VehicleBrandSchema(VehicleBrandBaseSchema):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
