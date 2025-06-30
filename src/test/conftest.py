import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from decimal import Decimal

from main import app
from core.database import get_db


@pytest.fixture
def mock_db_session():
    """Mock de la sesión de base de datos."""
    session = Mock(spec=Session)
    session.query = Mock()
    session.add = Mock()
    session.commit = Mock()
    session.refresh = Mock()
    session.delete = Mock()
    session.filter = Mock()
    session.first = Mock()
    session.all = Mock()
    return session


@pytest.fixture
def client(mock_db_session):
    """Cliente de prueba con base de datos mockeada."""

    def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_brand_data():
    """Datos de ejemplo para una marca."""
    return {
        "id": 1,
        "name": "Toyota",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }


@pytest.fixture
def sample_model_data():
    """Datos de ejemplo para un modelo."""
    return {
        "id": 1,
        "name": "Corolla",
        "average_price": Decimal("250000.50"),
        "brand_id": 1,
        "is_active": True,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }


@pytest.fixture
def sample_brands_list():
    """Lista de marcas de ejemplo."""
    return [
        {
            "id": 1,
            "name": "Toyota",
            "is_active": True,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        },
        {
            "id": 2,
            "name": "Honda",
            "is_active": True,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        },
    ]


@pytest.fixture
def sample_models_list():
    """Lista de modelos de ejemplo."""
    return [
        {
            "id": 1,
            "name": "Corolla",
            "average_price": Decimal("250000.50"),
            "brand_id": 1,
            "is_active": True,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        },
        {
            "id": 2,
            "name": "Camry",
            "average_price": Decimal("350000.75"),
            "brand_id": 1,
            "is_active": True,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        },
    ]
