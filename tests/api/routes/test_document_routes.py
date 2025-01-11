from datetime import datetime

import pytest
from fastapi import FastAPI, UploadFile
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, create_autospec

from app.api.endpoints import DocumentRoutes
from api.schemas.document_schemas import Document
from crud.document_crud import DocumentCRUD
from dependencies import Dependency


@pytest.fixture
def client_success():
    app = FastAPI()
    sample_document = Document(id=1, file_name="test_file.txt", file_type="text/plain", upload_timestamp=datetime(2022, 1, 1))

    # Create a mock for the DocumentCRUD
    mock_document_crud = create_autospec(DocumentCRUD)
    mock_document_crud.return_value.create_document.return_value = sample_document
    mock_document_crud.return_value.get_documents.return_value = [sample_document]

    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)

    # Initialize the DocumentRoutes with mocked dependencies
    document_routes = DocumentRoutes(dependency=mock_dependency, document_crud=mock_document_crud)

    # Include the router in the FastAPI app
    app.include_router(document_routes.router)

    return TestClient(app)

@pytest.fixture
def client_exception():
    app = FastAPI()
    sample_document = Document(id=1, file_name="test_file.txt", file_type="text/plain", upload_timestamp=datetime(2022, 1, 1))

    # Create a mock for the DocumentCRUD
    mock_document_crud = create_autospec(DocumentCRUD)
    mock_document_crud.return_value.create_document.side_effect = Exception("Simulated error")
    mock_document_crud.return_value.get_documents.side_effect = Exception("Simulated error")

    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)

    # Initialize the DocumentRoutes with mocked dependencies
    document_routes = DocumentRoutes(dependency=mock_dependency, document_crud=mock_document_crud)

    # Include the router in the FastAPI app
    app.include_router(document_routes.router)

    return TestClient(app)


def test_create_document(client_success):
    """Test successful document creation."""
    # Define the upload document data
    file_data = {
        "file": ("test_file.txt", b"Test file content", "text/plain")
    }

    # Send a POST request to create a document
    response = client_success.post("/api/upload/", files=file_data)

    # Assert the response status code is 200
    assert response.status_code == 200

    # Get the response JSON content
    response_data = response.json()

    # Check that the file details in the response match the uploaded file details
    assert response_data["file_name"] == "test_file.txt"
    assert response_data["file_type"] == "text/plain"
    assert response_data["parsed_text"] is None  # Assuming parsed_text is not set during upload

    # Optionally, check other attributes like `upload_timestamp`
    assert "upload_timestamp" in response_data

    # Further assertions can be added as needed, such as checking the database record

def test_create_document_exception(client_exception):
    """Test handling of exceptions during document creation."""
    # Define the upload document data
    # For example, passing an unsupported file type or no file at all
    file_data = {
        "file": ( b"", "text/plain")  # Simulate an empty file, can also test with no file
    }

    # Send a POST request to create a document
    response = client_exception.post("/api/upload/", files=file_data)

    # Assert that the status code is 500 if something goes wrong in the server-side logic
    assert response.status_code != 200

def test_read_documents(client_success):
    """Test reading documents successfully."""
    pass
def test_read_documents_exception(client_exception):
    """Test handling of exceptions during reading documents."""
    pass
