import os
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import JSONResponse

from api.schemas.parsed_document_schema import ParsedDocument
from app.crud.document_crud import DocumentCRUD
from app.dependencies import Dependency


class ParsedDocumentRoutes:
    def __init__(self, dependency: Dependency, parsed_document_crud=ParsedDocumentCRUD):
        self.router = APIRouter()
        self.db = dependency.get_db()
        self.parsed_document_crud = parsed_document_crud

        #TODO
        @self.router.post("/api/documents/{document_id}/parse", response_model=ParsedDocument)
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

                if not os.path.exists("/Users/denizcingoez/Documents/workspace/daiky/daiky-document-service/uploads"):
                    os.makedirs('/Users/denizcingoez/Documents/workspace/daiky/daiky-document-service/uploads')

                # Define the location where the file will be saved
                file_location = f"/Users/denizcingoez/Documents/workspace/daiky/daiky-document-service/uploads/{file_name}"

                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_location), exist_ok=True)

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


        @self.router.get("/api/document/", response_model=list[Document])
        def read_document():
            pass
