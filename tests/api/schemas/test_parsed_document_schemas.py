
from api.schemas.parsed_document_schema import ParsedDocument

def test_parsed_document_model_valid():
    document = ParsedDocument(summary="This is a test summary", chunks= ['chunk'])

    assert document.summary == "This is a test summary"
    assert document.chunks == ['chunk']
