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

#### DB SETUP
1. Open a new terminal window.
2. Run the `init_db_script` script to initialize the database.
3. To verify if the database was successfully created, start PostgreSQL by running the following command:
   
   ```bash
   psql
4. List all available databases and check if the daiky_document_service database exists with the command:
   ```bash
     \l
5. To connect to the daiky_document_service database, run:
    ```bash
   CREATE DATABASE daiky_document_service;

6. Once connected, check if the documents table exists by running:
    ```bash
   \dt

### Start
uvicorn app.main:app --reload
### Testing
pytest --cov=app tests/

pytest --cov=app --cov-report=term-missing

pytest --cov=app --cov-report=html tests/
### License
This project is licensed under the MIT License. See the LICENSE file for details.
