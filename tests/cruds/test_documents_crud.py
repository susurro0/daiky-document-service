from datetime import datetime

import pytest
from unittest.mock import MagicMock, patch

from fastapi import UploadFile

from api.schemas.document_schemas import DocumentCreate
from crud.document_crud import DocumentCRUD
from models.document_models import Document


@pytest.fixture
def mock_database():
    # Create a mock Database instance
    db_mock = MagicMock()
    return db_mock

@pytest.fixture
def document_crud(mock_database):
    return DocumentCRUD(mock_database)  # Replace DocumentCRUD with your actual class

@pytest.fixture
def mock_document():
    return MagicMock(spec=Document)

def test_create_document(document_crud, mock_document):
    # Arrange
    file = UploadFile(filename="test.txt", file=b"Hello, World!")
    document_data = DocumentCreate(
        file=file,
        file_name="test_file.txt",
        file_type="text/plain",
        upload_timestamp=datetime(2022, 1, 1)
    )
    with patch('app.models.document_models.Document.create', return_value=mock_document) as mock_create:
        # Act
        created_document = document_crud.create_document(document_data)

        # Assert
        mock_create.assert_called_once()
        assert created_document == mock_document

def test_get_documents(document_crud, mock_document):
    # Arrange
    with patch('app.models.document_models.Document.select', return_value=[mock_document]) as mock_select:
        # Act
        documents = document_crud.get_documents()

        # Assert
        mock_select.assert_called_once()
        assert documents == [mock_document]

def test_get_document_found(document_crud, mock_document):
    # Arrange
    document_id = 1
    with patch('app.models.document_models.Document.get_or_none', return_value=mock_document) as mock_get:
        # Act
        document = document_crud.get_document(document_id)

        # Assert
        mock_get.assert_called_once_with(Document.id == document_id)
        assert document == mock_document

def test_get_document_not_found(document_crud):
    # Arrange
    document_id = 999  # Assume this document does not exist
    with patch('app.models.document_models.Document.get_or_none', return_value=None) as mock_get:
        # Act
        document = document_crud.get_document(document_id)

        # Assert
        mock_get.assert_called_once_with(Document.id == document_id)
        assert document is None

def test_update_document_found(document_crud, mock_document):
    # Arrange
    document_id = 1
    file = UploadFile(filename="test.txt", file=b"Hello, World!")
    document_data = DocumentCreate(
        file=file,
        file_name="test_file.txt",
        file_type="text/plain",
        upload_timestamp=datetime(2022, 1, 1)
    )
    with patch('app.models.document_models.Document.get_or_none', return_value=mock_document) as mock_get, \
         patch.object(mock_document, 'save') as mock_save:
        # Act
        updated_document = document_crud.update_document(document_id, document_data)

        # Assert
        mock_get.assert_called_once_with(Document.id == document_id)
        assert updated_document == mock_document
        mock_save.assert_called_once()  # Ensure save was called

def test_update_document_not_found(document_crud):
    # Arrange
    document_id = 999  # Assume this document does not exist
    file = UploadFile(filename="test.txt", file=b"Hello, World!")
    document_data = DocumentCreate(
        file=file,
        file_name="test_file.txt",
        file_type="text/plain",
        upload_timestamp=datetime(2022, 1, 1)
    )
    with patch('app.models.document_models.Document.get_or_none', return_value=None) as mock_get:
        # Act
        updated_document = document_crud.update_document(document_id, document_data)

        # Assert
        mock_get.assert_called_once_with(Document.id == document_id)
        assert updated_document is None  # No document found, so return should be None

def test_delete_document_found(document_crud, mock_document):
    # Arrange
    document_id = 1
    with patch('app.models.document_models.Document.get_or_none', return_value=mock_document) as mock_get, \
         patch.object(mock_document, 'delete_instance') as mock_delete:
        # Act
        result = document_crud.delete_document(document_id)

        # Assert
        mock_get.assert_called_once_with(Document.id == document_id)
        mock_delete.assert_called_once()
        assert result is True

def test_delete_document_not_found(document_crud):
    # Arrange
    document_id = 999  # Assume this document does not exist
    with patch('app.models.document_models.Document.get_or_none', return_value=None) as mock_get:
        # Act
        result = document_crud.delete_document(document_id)

        # Assert
        mock_get.assert_called_once_with(Document.id == document_id)
        assert result is False
