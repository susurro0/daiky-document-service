
from api.schemas.parsed_document_schema import ParsedDocument

def test_parsed_document_model_valid():
    document = ParsedDocument(text="This is a test document")

    assert document.text == "This is a test document"
