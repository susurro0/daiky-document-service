from datetime import datetime
from logging import raiseExceptions

import pytest
from fastapi import FastAPI, UploadFile
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, create_autospec, patch

from app.api.endpoints import DocumentRoutes
from app.api.schemas.document_schemas import Document
from app.crud.document_crud import DocumentCRUD
from app.dependencies import Dependency


# Mock data
sample_document_pdf = Document(id=1, file_name="dummy.pdf", file_type="PDF", upload_timestamp=datetime(2022, 1, 1))
sample_document_docx = Document(id=2, file_name="dummy.docx", file_type="DOCX", upload_timestamp=datetime(2022, 1, 1))
sample_document_pptx = Document(id=909999, file_name="dummy.pptx", file_type="PPTX", upload_timestamp=datetime(2022, 1, 1))
sample_document_txt = Document(id=4, file_name="dummy.txt", file_type="txt", upload_timestamp=datetime(2022, 1, 1))


@pytest.fixture
def client_success():
    app = FastAPI()
    sample_document = Document(id=1, file_name="test_file.docx", file_type="docx", upload_timestamp=datetime(2022, 1, 1))

    # Create a mock for the DocumentCRUD
    mock_document_crud = create_autospec(DocumentCRUD)
    mock_document_crud.return_value.create_document.return_value = sample_document
    mock_document_crud.return_value.get_document.side_effect = sample_document_pdf
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
    sample_document = Document(id=1, file_name="test_file.pdf", file_type="pdf", upload_timestamp=datetime(2022, 1, 1))

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

@pytest.fixture
def client_parsed_success():
    app = FastAPI()

    # Create a mock for the DocumentCRUD
    mock_document_crud = create_autospec(DocumentCRUD)

    # Ensure the mock returns actual document objects with file_type attributes
    def mock_get_document(document_id: int):
        if document_id == 1:
            return sample_document_pdf
        if document_id == 2:
            return sample_document_docx
        if document_id == 909999:
            return sample_document_pptx
        if document_id == 4:
            return sample_document_txt
        return None

    mock_document_crud.get_document.side_effect = mock_get_document

    mock_dependency = MagicMock(spec=Dependency)
    document_routes = DocumentRoutes(dependency=mock_dependency, document_crud=mock_document_crud)
    app.include_router(document_routes.router)

    return TestClient(app)

@pytest.fixture
def client_parsed_exception():
    app = FastAPI()

    mock_document_crud = create_autospec(DocumentCRUD)

    # Ensure the mock returns actual document objects with file_type attributes
    def mock_get_document(document_id: int):
        if document_id == 1:
            return Exception("Simulated error")
        return None

    mock_document_crud.get_document.side_effect = mock_get_document

    mock_dependency = MagicMock(spec=Dependency)
    document_routes = DocumentRoutes(dependency=mock_dependency, document_crud=mock_document_crud)
    app.include_router(document_routes.router)

    return TestClient(app)
def test_create_document(client_success):
    """Test successful document creation."""
    # Define the upload document data
    file_data = {
        "file": ("test_file.pdf", b"Test file content", "application/pdf")
    }


    # Send a POST request to create a document
    response = client_success.post("/api/upload/", files=file_data)

    # Assert the response status code is 200
    assert response.status_code == 200

    # Get the response JSON content
    response_data = response.json()

    # Check that the file details in the response match the uploaded file details
    assert response_data["file_name"] == "test_file.pdf"
    assert response_data["file_type"] == "PDF"
    assert response_data["parsed_text"] is None  # Assuming parsed_text is not set during upload

    # Optionally, check other attributes like `upload_timestamp`
    assert "upload_timestamp" in response_data
    # Further assertions can be added as needed, such as checking the database record

def test_create_document_exception(client_exception):
    """Test handling of exceptions during document creation."""
    # Define the upload document data
    # For example, passing an unsupported file type or no file at all
    file_data = {
        "file": ("test_file.txt", b"Test file content", "text/plain")
    }
    with patch('app.crud.document_crud.DocumentCRUD.create_document', side_effect=Exception("Simulated error")):

        # Send a POST request to create a document
        response = client_exception.post("/api/upload/", files=file_data)

        # Assert that the status code is 500 if something goes wrong in the server-side logic
        assert response.status_code == 500
        assert response.json() == {'detail': 'An error occurred while uploading the file.'}

# Test for successful document parsing (PDF)
def test_parse_pdf_document(client_parsed_success):
    response = client_parsed_success.get("/api/documents/1/parse")
    assert response.status_code == 200
    assert response.json() == {'chunks': ['Dummy PDF file'], 'summary': ''}

def test_parse_document_not_found(client_parsed_success):
    response = client_parsed_success.get("/api/documents/999/parse")  # Use a non-existent document ID
    assert response.status_code == 404
    assert response.json() == {"detail": "Document not found"}

def test_parse_docx_document(client_parsed_success):
    response = client_parsed_success.get("/api/documents/2/parse")
    assert response.status_code == 200

def test_parse_pptx_document(client_parsed_success):
    response = client_parsed_success.get("/api/documents/909999/parse")
    assert response.status_code == 200
    assert response.json() == {'chunks': ['Dummy pptx file\n'], 'summary': ''}

def test_parse_document_unsupported_format(client_parsed_success):

    response = client_parsed_success.get("/api/documents/4/parse")
    assert response.status_code == 415
    assert response.json()["detail"] == "Unsupported file format"
def test_internal_server_error_parse_text(client_parsed_exception):
    # Send a POST request to create a document
    response = client_parsed_exception.get("/api/documents/1/parse")
    assert response.status_code == 500
    assert response.json() == {"detail": "An error occurred while parsing the document."}