from sqlalchemy import Column, Integer, Boolean, DateTime
from shared.dates import now


class BaseModelMixin:
    """
    Mixin que añade columnas comunes a los modelos.
    """

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=now)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now)
