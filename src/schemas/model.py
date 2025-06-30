from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal

from core.constants import MIN_AVERAGE_PRICE


class VehicleModelBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    average_price: float | None = Field(
        None,
        gt=MIN_AVERAGE_PRICE,
        description="El precio debe ser mayor que {MIN_AVERAGE_PRICE}.",
    )


class VehicleModelCreateMigrationSchema(VehicleModelBaseSchema):
    brand_id: int


class VehicleModelCreateSchema(VehicleModelBaseSchema):
    pass


class VehicleModelUpdateSchema(BaseModel):
    average_price: float | None = Field(
        None,
        gt=MIN_AVERAGE_PRICE,
        description="El precio debe ser mayor que {MIN_AVERAGE_PRICE}.",
    )


class VehicleModelSchema(VehicleModelBaseSchema):
    id: int
    brand_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VehicleModelSummarySchema(BaseModel):
    id: int
    name: str
    average_price: Decimal | None = None

    model_config = ConfigDict(from_attributes=True)
