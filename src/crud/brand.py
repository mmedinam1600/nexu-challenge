"""
Este módulo contiene la clase de repositorio para las operaciones CRUD
del modelo VehicleBrandModel.
"""

import typing as t
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from models.brand import VehicleBrandModel
from schemas.brand import (
    VehicleBrandUpdateSchema,
    VehicleBrandCreateSchema,
)


class CRUDBrand:
    def __init__(self, model: type[VehicleBrandModel]):
        self.model = model

    def bulk_insert(self, db: Session, *, brands_data: list[VehicleBrandCreateSchema]):
        """
        Inserta múltiples marcas en la base de datos.
        """
        if not brands_data:
            return

        brands_dict = [brand.model_dump() for brand in brands_data]
        stmt = insert(self.model).values(brands_dict)
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])
        db.execute(stmt)
        db.commit()

    @staticmethod
    def get_all(db: Session) -> t.List[VehicleBrandModel]:
        """Obtiene todas las marcas de vehículos."""
        return db.query(VehicleBrandModel).all()

    @staticmethod
    def get_by_id(db: Session, brand_id: int) -> t.Optional[VehicleBrandModel]:
        """Obtiene una marca de vehículo por su ID."""
        return (
            db.query(VehicleBrandModel).filter(VehicleBrandModel.id == brand_id).first()
        )

    @staticmethod
    def get_by_name(db: Session, name: str) -> t.Optional[VehicleBrandModel]:
        return (
            db.query(VehicleBrandModel).filter(VehicleBrandModel.name == name).first()
        )

    @staticmethod
    def create(db: Session, brand: VehicleBrandCreateSchema) -> VehicleBrandModel:
        """Crea una nueva marca de vehículo."""
        db_brand = VehicleBrandModel(**brand.model_dump())
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        return db_brand

    @staticmethod
    def update(
        db: Session, db_brand: VehicleBrandModel, brand_in: VehicleBrandUpdateSchema
    ) -> VehicleBrandModel:
        """Actualiza una marca de vehículo existente."""
        update_data = brand_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_brand, key, value)

        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        return db_brand

    @staticmethod
    def delete(db: Session, brand_id: int) -> t.Optional[VehicleBrandModel]:
        """Elimina una marca de vehículo por su ID."""
        db_brand = CRUDBrand.get_by_id(db, brand_id)
        if db_brand:
            db.delete(db_brand)
            db.commit()
        return db_brand
