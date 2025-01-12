import os
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import JSONResponse

from api.schemas.parsed_document_schema import ParsedDocument
from app.api.schemas.document_schemas import DocumentCreate, Document
from app.crud.document_crud import DocumentCRUD
from app.dependencies import Dependency
from PyPDF2 import PdfReader


class DocumentRoutes:
    def __init__(self, dependency: Dependency, document_crud=DocumentCRUD):
        self.router = APIRouter()
        self.db = dependency.get_db()
        self.document_crud = document_crud

        #TODO
        @self.router.post("/api/upload/", response_model=Document)
        def upload_file(file: UploadFile = File(...)):
            """
            Endpoint to upload a file and save its details in the database.

            Args:
                file (UploadFile): The file to be uploaded.

            Returns:
                Document: The document object with saved information.
            """
            try:
                # Extract file details
                file_name = file.filename
                file_type = file.content_type
                upload_timestamp = datetime.now()

                # Define the location where the file will be saved
                file_location = f"uploads/{file_name}"

                # Ensure the directory exists
                if not os.path.exists(os.path.dirname(file_location)):
                    os.makedirs(os.path.dirname(file_location), exist_ok=True)
                os.chmod(os.path.dirname(file_location), 0o777)

                # Check if the file exists and handle overwrite logic
                if os.path.exists(file_location):
                    # Log the overwrite action if needed
                    print(f"File {file_name} already exists. Overwriting...")

                # Save the file to the specified location
                with open(file_location, "wb") as f:
                    f.write(file.file.read())

                # Create the document object for saving to the database
                document_create = DocumentCreate(
                    file=file,
                    file_name=file_name,
                    file_type=file_type,
                    upload_timestamp=upload_timestamp,
                )
                # Assuming we have an instance of DocumentCRUD
                document_crud = DocumentCRUD(db=self.db)  # Use the proper db connection here
                saved_document = document_crud.create_document(document_create)

                # Return the saved document as a response
                return JSONResponse(
                    content={
                        "id": saved_document.id,
                        "file_name": saved_document.file_name,
                        "file_type": saved_document.file_type,
                        "upload_timestamp": saved_document.upload_timestamp.isoformat(),
                        "parsed_text": saved_document.parsed_text,
                    },
                    status_code=200,
                )

            except Exception as e:
                print(f"Failed to upload file: {e}")  # Replace with proper logging in production
                raise HTTPException(
                    status_code=500, detail="An error occurred while uploading the file."
                )

        @self.router.post("/api/documents/{document_id}/parse", response_model=ParsedDocument)
        def parse_document(document_id: int):
            try:
                # Retrieve the document from the database
                document = self.document_crud.get_document(document_id)
                if document is None:
                    raise HTTPException(status_code=404, detail="Document not found")

                # Parse the document
                file_location = f"uploads/{document.file_name}"
                if document.file_type == "application/pdf":
                    with open(file_location, "rb") as f:
                        pdf_reader = PdfReader(f)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text()
                        return ParsedDocument(text=text)
                elif document.file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    from docx import Document as DocxDocument
                    docx = DocxDocument(file_location)
                    text = ""
                    for para in docx.paragraphs:
                        text += para.text
                    return ParsedDocument(text=text)
                elif document.file_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
                    from pptx import Presentation
                    pptx = Presentation(file_location)
                    text = ""
                    for slide in pptx.slides:
                        for shape in slide.shapes:
                            if hasattr(shape, "text"):
                                text += shape.text
                    return ParsedDocument(text=text)
                else:
                    raise HTTPException(status_code=415, detail="Unsupported file format")

            except Exception as e:
                if isinstance(e, HTTPException):
                    # If it is, re-raise the same HTTPException
                    raise e
                else:
                    # Otherwise, raise a new HTTPException with a generic message
                    print(f"Failed to parse document: {e}")  # Replace with proper logging in production
                    raise HTTPException(
                        status_code=500,
                        detail="An error occurred while parsing the document."
                    )

