from typing import Optional, List
from api.schemas.document_schemas import DocumentCreate
from models.document_models import Document


class DocumentCRUD:
    def __init__(self, db):
        self.db = db  # The db is now an instance of SqliteDatabase

    def create_document(self, document: DocumentCreate) -> Document:
        db_document = Document.create(**document.model_dump())
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
