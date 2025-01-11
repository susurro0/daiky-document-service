from datetime import datetime

import pytest
from fastapi import UploadFile
from pydantic import ValidationError
from enum import Enum

from app.api.schemas.document_schemas import DocumentBase, DocumentCreate, Document


def test_document_base_model_valid():
    document = DocumentBase(file_name="test_file.txt", file_type="text/plain", upload_timestamp=datetime(2022, 1, 1))
    assert document.file_name == "test_file.txt"
    assert document.file_type == "text/plain"
    assert document.upload_timestamp == datetime(2022, 1, 1)

def test_document_create_model():
    file = UploadFile(filename="test.txt", file=b"Hello, World!")

    document_create = DocumentCreate(file=file, file_name="test_file.txt", file_type="text/plain", upload_timestamp=datetime(2022, 1, 1))
    assert document_create.file_name == "test_file.txt"
    assert document_create.file_type == "text/plain"
    assert document_create.upload_timestamp == datetime(2022, 1, 1)

def test_document_model_valid():
    document = Document(id=1, file_name="test_file.txt", file_type="text/plain", upload_timestamp=datetime(2022, 1, 1))
    assert document.id == 1
    assert document.file_name == "test_file.txt"
    assert document.file_type == "text/plain"
    assert document.upload_timestamp == datetime(2022, 1, 1)

def test_document_model_invalid_id():
    with pytest.raises(ValidationError) as exc_info:
        Document(id="one", file_name="test_file.txt", file_type="text/plain",upload_timestamp=datetime(2022, 1, 1))
    assert "should be a valid integer" in str(exc_info.value)

