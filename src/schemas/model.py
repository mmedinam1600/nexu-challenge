from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID


class VehicleModelBaseSchema(BaseModel):
    name: str
    average_price: Optional[Decimal] = Field(
        default=None,
        gt=100000,
        description="El precio promedio del modelo, debe ser mayor a 100,000",
    )


class VehicleModelCreateSchema(VehicleModelBaseSchema):
    pass


class VehicleModelUpdateSchema(BaseModel):
    name: Optional[str] = None
    average_price: Optional[Decimal] = Field(
        default=None,
        gt=100000,
        description="El precio promedio del modelo, debe ser mayor a 100,000",
    )
    is_active: Optional[bool] = None


class VehicleModelSchema(VehicleModelBaseSchema):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
