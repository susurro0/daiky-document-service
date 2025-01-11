# Document Service

## Overview
The Document Service is a RESTful API that allows users to upload, store, and parse documents. The service supports **PDF**, **Word (.docx)**, and **PowerPoint (.pptx)** file formats.

## Features
- Document upload and storage
- Document parsing and text extraction
- Support for PDF, Word (.docx), and PowerPoint (.pptx) file formats
- RESTful API with JSON responses

## API Endpoints

### 1. Upload Document
- **Endpoint**: `POST /documents`
- **Request Body**: 
  - `document` (file upload)
- **Response**:
  ```json
  {
    "document_id": "<id>"
  }
  
### 2. Parse Document
- **Endpoint**: POST /documents/{id}/parse
- **Request Body**: None
- **Response**:
  ```json
   {"text": <extracted text>}
  
### Requirements
- Python 3.9+
- FastAPI
- PostgreSQL

### Installation

### Start
uvicorn app.main:app --reload
### Testing
pytest --cov=app tests/

pytest --cov=app --cov-report=term-missing

pytest --cov=app --cov-report=html tests/
### License
This project is licensed under the MIT License. See the LICENSE file for details.
