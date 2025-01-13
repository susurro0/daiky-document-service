from pydantic import BaseModel, ConfigDict


class ParsedDocument(BaseModel):
    text: str
    summary: str
    model_config = ConfigDict()


class ParseDocumentRequest(BaseModel):
    documentId: int