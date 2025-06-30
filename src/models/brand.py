from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base
from .mixins import BaseModelMixin


class VehicleBrandModel(BaseModelMixin, Base):
    name = Column(String(100), index=True, nullable=False)

    models = relationship("VehicleModelModel", back_populates="brand")

    __tablename__ = "brands"
    __table_args__ = (
        UniqueConstraint("name", name="uq_vehicle_brand_name"),
        {"schema": "vehicle"},
    )

    def __repr__(self) -> str:
        return f"<VehicleBrandModel(id={self.id}, name={self.name}, is_active={self.is_active})>"
