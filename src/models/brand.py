from sqlalchemy import Column, String, Numeric, UniqueConstraint, CheckConstraint
from core.database import Base
from .mixins import BaseModelMixin


class VehicleBrandModel(BaseModelMixin, Base):
    name = Column(String(100), index=True, nullable=False)
    average_price = Column(
        Numeric(10, 2),
        CheckConstraint("average_price > 100000", name="check_brand_average_price"),
        index=True,
        nullable=True,
    )

    __tablename__ = "brands"
    __table_args__ = (
        UniqueConstraint("name", name="uq_vehicle_brand_name"),
        {"schema": "vehicle"},
    )

    def __repr__(self) -> str:
        return f"<VehicleBrandModel(id={self.id}, name={self.name}, average_price={self.average_price}, is_active={self.is_active})>"
