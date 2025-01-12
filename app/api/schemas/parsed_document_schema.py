from pydantic import BaseModel, ConfigDict


class ParsedDocument(BaseModel):
    text: str
    model_config = ConfigDict()