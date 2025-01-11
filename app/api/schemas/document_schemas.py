from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    file_name: str
    file_type: str
    upload_timestamp: datetime
    parsed_text: Optional[str] = None

    model_config = ConfigDict()

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    parsed_text: Optional[str] = None

class Document(DocumentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

