from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from core.constants import MIN_AVERAGE_PRICE


class VehicleModelBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    average_price: float | None = Field(
        None,
        gt=MIN_AVERAGE_PRICE,
        description="El precio debe ser mayor que {MIN_AVERAGE_PRICE}.",
    )


class VehicleModelCreateSchema(VehicleModelBaseSchema):
    brand_id: int


class VehicleModelUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)


class VehicleModelSchema(VehicleModelBaseSchema):
    id: int
    brand_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
