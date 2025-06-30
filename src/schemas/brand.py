from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


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
    name: Optional[str] = None
    is_active: Optional[bool] = None


class VehicleBrandSchema(VehicleBrandBaseSchema):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
