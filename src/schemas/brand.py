from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class VehicleBrandBaseSchema(BaseModel):
    name: str


class VehicleBrandCreateSchema(VehicleBrandBaseSchema):
    def __eq__(self, other) -> bool:
        if not isinstance(other, VehicleBrandBaseSchema):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class VehicleBrandUpdateSchema(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class VehicleBrandSchema(VehicleBrandBaseSchema):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VehicleBrandWithAveragePriceSchema(BaseModel):
    id: int
    name: str
    average_price: Decimal | None = None

    model_config = ConfigDict(from_attributes=True)
