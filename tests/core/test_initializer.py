import pytest
from unittest.mock import patch, MagicMock
from app.core.initializer import AppInitializer  # Adjust the import based on your structure
from app.db.database import database_instance, Database
from models.document_models import Document


@pytest.fixture
def mock_app():
    from fastapi import FastAPI
    app = FastAPI()
    app.state = MagicMock()  # Ensure state can be mocked
    return app

@pytest.fixture
def mock_database():
    # Create a mock Database instance
    db_mock = MagicMock(spec=Database)
    db_mock.database = MagicMock()  # Mock the database attribute
    db_mock.connect = MagicMock()  # Mock the connect method
    db_mock.close = MagicMock()  # Mock the close method
    return db_mock
@pytest.fixture
def app_initializer(mock_app, mock_database):
    return AppInitializer(mock_app, mock_database)

def test_initialize_spy(app_initializer, mock_database):
    app_initializer.initialize()
    assert app_initializer.app.state.db == mock_database

