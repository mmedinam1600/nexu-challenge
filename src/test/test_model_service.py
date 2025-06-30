import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from services.model_service import ModelService
from schemas.model import VehicleModelUpdateSchema


class TestModelService:

    def test_get_all_models_filtered_success(self, mock_db_session, sample_models_list):
        """Prueba obtener todos los modelos con filtros exitosamente."""
        # Arrange
        mock_models = [Mock(**model) for model in sample_models_list]
        mock_db_session.query.return_value.all.return_value = mock_models

        # Act
        result = ModelService.get_all_models_filtered(mock_db_session)

        # Assert
        assert result == mock_models
        mock_db_session.query.assert_called_once()

    def test_get_all_models_filtered_with_greater_filter(self, mock_db_session):
        """Prueba obtener modelos con filtro de precio mayor."""
        # Arrange
        greater_price = 200000.0
        mock_models = [Mock(id=1, name="Corolla", average_price=250000.50)]
        # Encadena el mock para .filter().all()
        mock_filter = Mock()
        mock_filter.all.return_value = mock_models
        mock_db_session.query.return_value.filter.return_value = mock_filter

        # Act
        result = ModelService.get_all_models_filtered(mock_db_session, greater=greater_price)

        # Assert
        assert result == mock_models
        mock_db_session.query.assert_called_once()

    def test_get_all_models_filtered_with_lower_filter(self, mock_db_session):
        """Prueba obtener modelos con filtro de precio menor."""
        # Arrange
        lower_price = 300000.0
        mock_models = [Mock(id=1, name="Corolla", average_price=250000.50)]
        mock_filter = Mock()
        mock_filter.all.return_value = mock_models
        mock_db_session.query.return_value.filter.return_value = mock_filter

        # Act
        result = ModelService.get_all_models_filtered(mock_db_session, lower=lower_price)

        # Assert
        assert result == mock_models
        mock_db_session.query.assert_called_once()

    def test_get_all_models_filtered_with_both_filters(self, mock_db_session):
        """Prueba obtener modelos con ambos filtros de precio."""
        # Arrange
        greater_price = 200000.0
        lower_price = 300000.0
        mock_models = [Mock(id=1, name="Corolla", average_price=250000.50)]
        # Encadena dos filtros
        mock_filter_1 = Mock()
        mock_filter_2 = Mock()
        mock_filter_2.all.return_value = mock_models
        mock_filter_1.filter.return_value = mock_filter_2
        mock_db_session.query.return_value.filter.return_value = mock_filter_1

        # Act
        result = ModelService.get_all_models_filtered(
            mock_db_session, greater=greater_price, lower=lower_price
        )

        # Assert
        assert result == mock_models
        mock_db_session.query.assert_called_once()

    def test_update_model_price_success(self, mock_db_session):
        """Prueba actualizar el precio de un modelo exitosamente."""
        # Arrange
        model_id = 1
        update_data = {"average_price": 300000.50}
        model_schema = VehicleModelUpdateSchema(**update_data)
        mock_model = Mock(id=model_id, name="Corolla", average_price=300000.50)
        
        with patch('services.model_service.CRUDModel.get_by_id', return_value=mock_model), \
             patch('services.model_service.CRUDModel.update', return_value=mock_model):
            
            # Act
            result = ModelService.update_model_price(mock_db_session, model_id, model_schema)

            # Assert
            assert result == mock_model

    def test_update_model_price_model_not_found(self, mock_db_session):
        """Prueba actualizar el precio de un modelo que no existe."""
        # Arrange
        model_id = 999
        update_data = {"average_price": 300000.50}
        model_schema = VehicleModelUpdateSchema(**update_data)
        
        with patch('services.model_service.CRUDModel.get_by_id', return_value=None):
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                ModelService.update_model_price(mock_db_session, model_id, model_schema)
            
            assert exc_info.value.status_code == 404
            assert f"El modelo con id '{model_id}' no existe." in str(exc_info.value.detail)

    def test_update_model_price_partial_update(self, mock_db_session):
        """Prueba actualización parcial del modelo."""
        # Arrange
        model_id = 1
        update_data = {"average_price": 300000.50}
        model_schema = VehicleModelUpdateSchema(**update_data)
        mock_model = Mock(id=model_id, name="Corolla", average_price=300000.50)
        
        with patch('services.model_service.CRUDModel.get_by_id', return_value=mock_model), \
             patch('services.model_service.CRUDModel.update', return_value=mock_model):
            
            # Act
            result = ModelService.update_model_price(mock_db_session, model_id, model_schema)

            # Assert
            assert result == mock_model

    def test_update_model_price_empty_update(self, mock_db_session):
        """Prueba actualización con datos vacíos."""
        # Arrange
        model_id = 1
        update_data = {}
        model_schema = VehicleModelUpdateSchema(**update_data)
        mock_model = Mock(id=model_id, name="Corolla", average_price=250000.50)
        
        with patch('services.model_service.CRUDModel.get_by_id', return_value=mock_model), \
             patch('services.model_service.CRUDModel.update', return_value=mock_model):
            
            # Act
            result = ModelService.update_model_price(mock_db_session, model_id, model_schema)

            # Assert
            assert result == mock_model 