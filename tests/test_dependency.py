# test_dependency.py
import pytest
from unittest.mock import MagicMock
from app.db.database import Database
from app.dependencies import Dependency


@pytest.fixture
def mock_database():
    # Create a mock Database instance
    db_mock = MagicMock(spec=Database)
    db_mock.database = MagicMock()  # Mock the database attribute
    db_mock.connect = MagicMock()  # Mock the connect method
    db_mock.close = MagicMock()  # Mock the close method
    return db_mock

@pytest.fixture
def dependency_instance(mock_database):
    # Create an instance of the Dependency class with the mocked Database
    return Dependency(mock_database)

def test_get_db_connects_and_yields_database(dependency_instance):
    # Arrange
    mock_db_instance = dependency_instance.db.database

    # Act
    db_gen = dependency_instance.get_db()
    database = next(db_gen)  # Get the yielded value

    # Assert
    assert dependency_instance.db.connect.called
    assert database == mock_db_instance

    # Clean up: close the generator to trigger cleanup
    db_gen.close()

def test_get_db_closes_connection(dependency_instance):
    # Arrange
    mock_db_instance = dependency_instance.db.database

    # Act
    db_gen = dependency_instance.get_db()
    next(db_gen)  # Get the yielded value
    db_gen.close()  # Close the generator to trigger cleanup

    # Assert
    assert dependency_instance.db.connect.called
    assert dependency_instance.db.close.called
