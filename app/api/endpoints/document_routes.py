from fastapi import APIRouter, HTTPException

from api.schemas.document_schemas import DocumentCreate, Document
from crud.document_crud import DocumentCRUD
from dependencies import Dependency

class DocumentRoutes:
    def __init__(self, dependency: Dependency, document_crud=DocumentCRUD):
        self.router = APIRouter()
        self.db = dependency.get_db()
        self.task_crud = document_crud

        #TODO
        @self.router.post("/api/document/", response_model=Document)
        def create_document(task: DocumentCreate):
            pass

        @self.router.get("/api/document/", response_model=list[Document])
        def read_document():
            pass
