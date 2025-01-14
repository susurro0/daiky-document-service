from typing import List

from pydantic import BaseModel, ConfigDict


class ParsedDocument(BaseModel):
    summary: str
    chunks: List[str]
    model_config = ConfigDict()


class ParseDocumentRequest(BaseModel):
    documentId: int