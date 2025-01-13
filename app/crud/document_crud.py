from typing import Optional, List
from app.api.schemas.document_schemas import DocumentCreate
from app.models.document_models import Document


class DocumentCRUD:
    def __init__(self, db):
        self.db = db  # The db is now an instance of SqliteDatabase

    def map_file_type(self, file_type: str) -> str:
        """
        Maps a full file type (MIME type) to a shorter version.

        Args:
        - file_type (str): The MIME type of the file.

        Returns:
        - str: The shortened version of the MIME type.
        """
        file_type_map = {
            "application/pdf": "PDF",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "DOCX",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": "PPTX",
            "application/msword": "DOC",  # Add more mappings as necessary
            "application/vnd.ms-excel": "XLS",  # Add more mappings as necessary
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "XLSX",
            "image/jpeg": "JPEG",
            "image/png": "PNG",
            # Add more mappings as needed
        }

        return file_type_map.get(file_type, "Unknown")  # Default to "Unknown" if no mapping found

    def create_document(self, document: DocumentCreate) -> Document:
        db_document = Document.create(
            file_name=document.file_name,
            file_type=self.map_file_type(document.file_type)
        )
        return db_document

    def get_documents(self) -> List[Document]:
        return list(Document.select())  # Returns all documents as a list

    def get_document(self, document_id: int) -> Optional[Document]:
        return Document.get_or_none(Document.id == document_id)  # Returns None if not found

    def update_document(self, document_id: int, document_data: DocumentCreate) -> Optional[Document]:
        db_document = Document.get_or_none(Document.id == document_id)
        if db_document:
            for key, value in document_data.model_dump().items():
                setattr(db_document, key, value)
            db_document.save()  # Save changes to the database
        return db_document

    def delete_document(self, document_id: int) -> bool:
        db_document = Document.get_or_none(Document.id == document_id)
        if db_document:
            db_document.delete_instance()  # Delete the document from the database
            return True
        return False
