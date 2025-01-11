import pytest
from unittest.mock import patch, MagicMock
from app.db.database import Database

@pytest.fixture
def mock_database():
    # Create a mock PostgresqlDatabase instance
    with patch('app.db.database.PostgresqlDatabase') as MockPostgresqlDatabase:
        mock_db_instance = MagicMock()
        MockPostgresqlDatabase.return_value = mock_db_instance
        yield mock_db_instance
@pytest.fixture
def database_instance(mock_database):
    # Create a Database instance using the mock database URL
    db_url = "postgresql://user:password@localhost/dbname"
    return Database(db_url)

def test_connect(mock_database, database_instance):
    # Act
    database_instance.connect()

    # Assert
    mock_database.connect.assert_called_once()

def test_close(mock_database, database_instance):
    # Arrange
    mock_database.is_closed.return_value = False

    # Act
    database_instance.close()

    # Assert
    mock_database.close.assert_called_once()

def test_close_already_closed(mock_database, database_instance):
    # Arrange
    mock_database.is_closed.return_value = True

    # Act
    database_instance.close()

    # Assert
    mock_database.close.assert_not_called()

def test_create_tables(mock_database, database_instance):
    # Arrange
    mock_models = []  # Replace with actual model classes if needed

    # Act
    database_instance.create_tables(mock_models)

    # Assert
    mock_database.create_tables.assert_called_once_with(mock_models, safe=True)
