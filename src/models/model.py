from sqlalchemy import (
    Column,
    String,
    Numeric,
    UniqueConstraint,
    CheckConstraint,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from core.constants import MIN_AVERAGE_PRICE
from core.database import Base
from .mixins import BaseModelMixin


class VehicleModelModel(BaseModelMixin, Base):
    name = Column(String(100), index=True, nullable=False)
    average_price = Column(
        Numeric(10, 2),
        CheckConstraint(
            f"average_price > {MIN_AVERAGE_PRICE}", name="check_model_average_price"
        ),
        index=True,
        nullable=True,
    )
    brand_id = Column(Integer, ForeignKey("vehicle.brands.id"), nullable=False)

    brand = relationship("VehicleBrandModel", back_populates="models")

    __tablename__ = "models"
    __table_args__ = (
        UniqueConstraint("name", name="uq_vehicle_model_name"),
        {"schema": "vehicle"},
    )

    def __repr__(self) -> str:
        return f"<VehicleModelModel(id={self.id}, name={self.name}, average_price={self.average_price}, is_active={self.is_active})>"
