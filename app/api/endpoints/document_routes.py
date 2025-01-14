import os
from datetime import datetime
from transformers import pipeline, AutoTokenizer
from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import JSONResponse

from app.api.schemas.parsed_document_schema import ParsedDocument
from app.api.schemas.document_schemas import DocumentCreate, Document
from app.crud.document_crud import DocumentCRUD
from app.dependencies import Dependency
from PyPDF2 import PdfReader


class DocumentRoutes:
    def __init__(self, dependency: Dependency, document_crud=DocumentCRUD):
        self.router = APIRouter()
        self.db = dependency.get_db()
        self.document_crud = document_crud
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        self.summarizer = pipeline("summarization")
        #TODO
        @self.router.post("/api/upload/", response_model=Document)
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
                # Define the location where the file will be saved
                file_location = f"uploads/{file_name}"

                # Ensure the directory exists
                if not os.path.exists(os.path.dirname(file_location)):
                    os.makedirs(os.path.dirname(file_location), exist_ok=True)
                os.chmod(os.path.dirname(file_location), 0o777)

                # Check if the file exists and handle overwrite logic
                if os.path.exists(file_location):
                    # Log the overwrite action if needed
                    print(f"File {file_name} already exists. Overwriting...")

                # Save the file to the specified location
                with open(file_location, "wb") as f:
                    f.write(file.file.read())

                # Parse the document if it's a PDF  'Create the document object for saving to the database
                document_create = DocumentCreate(
                    file=file,
                    file_name=file_name,
                    file_type=file_type,
                    upload_timestamp=upload_timestamp,
                )
                print(document_create.upload_timestamp)

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

        # @self.router.post("/api/documents/{document_id}/parse", response_model=ParsedDocument)
        # def parse_document(document_id: int):
        #     try:
        #         # Retrieve the document from the database
        #         document = self.document_crud.get_document(self, document_id=document_id)
        #         if document is None:
        #             raise HTTPException(status_code=404, detail="Document not found")
        #
        #         # Parse the document
        #         file_location = f"uploads/{document.file_name}"
        #         text = ""
        #         if document.file_type == "PDF":
        #             with open(file_location, "rb") as f:
        #                 pdf_reader = PdfReader(f)
        #                 text = ""
        #                 for page in pdf_reader.pages:
        #                     text += page.extract_text()
        #         elif document.file_type == "DOCX":
        #             from docx import Document as DocxDocument
        #             docx = DocxDocument(file_location)
        #             text = ""
        #             for para in docx.paragraphs:
        #                 text += para.text
        #         elif document.file_type == "PPTX":
        #             from pptx import Presentation
        #             pptx = Presentation(file_location)
        #             text = ""
        #             for slide in pptx.slides:
        #                 for shape in slide.shapes:
        #                     if hasattr(shape, "text"):
        #                         text += shape.text
        #         else:
        #             raise HTTPException(status_code=415, detail="Unsupported file format")
        #         print(type(text))
        #         summary = self.summarizer(text, max_length=150, min_length=25, do_sample=False)
        #         print(summary)
        #         return ParsedDocument(text=text, summary=summary[0]['summary_text'])
        #     except Exception as e:
        #         if isinstance(e, HTTPException):
        #             # If it is, re-raise the same HTTPException
        #             raise e
        #         else:
        #             # Otherwise, raise a new HTTPException with a generic message
        #             print(f"Failed to parse document: {e}")  # Replace with proper logging in production
        #             raise HTTPException(
        #                 status_code=500,
        #                 detail="An error occurred while parsing the document."
        #             )

        def __split_with_overlap(text, tokenizer_name="bert-base-uncased", max_length=256, overlap=50):
            """
            Splits text into chunks using a tokenizer with overlap.

            Args:
                text (str): The input text to be split.
                tokenizer_name (str): Name of the tokenizer (e.g., "bert-base-uncased").
                max_length (int): Maximum token length for each chunk.
                overlap (int): Number of overlapping tokens between chunks.

            Returns:
                List[str]: List of text chunks.
            """
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
            tokens = tokenizer.encode(text, add_special_tokens=False)

            chunks = []
            for i in range(0, len(tokens), max_length - overlap):
                chunk_tokens = tokens[i:i + max_length]
                chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
                chunks.append(chunk_text)

            return chunks

        #
        @self.router.get("/api/documents/{document_id}/parse", response_model=ParsedDocument)
        def parse_document(document_id: int):
            try:
                # Step 1: Retrieve the document from the database
                document = self.document_crud.get_document(self, document_id=document_id)
                if document is None:
                    raise HTTPException(status_code=404, detail="Document not found")

                # Step 2: Extract text from the document
                file_location = f"uploads/{document.file_name}"
                text = ""
                if document.file_type == "PDF":
                    with open(file_location, "rb") as f:
                        from PyPDF2 import PdfReader
                        pdf_reader = PdfReader(f)
                        text = "".join(page.extract_text() for page in pdf_reader.pages)
                elif document.file_type == "DOCX":
                    from docx import Document as DocxDocument
                    docx = DocxDocument(file_location)
                    text = "\n".join(para.text for para in docx.paragraphs)
                elif document.file_type == "PPTX":
                    from pptx import Presentation
                    pptx = Presentation(file_location)
                    text = "\n".join(
                        shape.text for slide in pptx.slides for shape in slide.shapes if hasattr(shape, "text")
                    )
                else:
                    raise HTTPException(status_code=415, detail="Unsupported file format")

                chunks = __split_with_overlap(text, max_length=128, overlap=25)
                summary = __summarize_text(text)

                return ParsedDocument(chunks=chunks, summary=summary)

            except Exception as e:
                if isinstance(e, HTTPException):
                    raise e
                else:
                    print(f"Failed to parse document: {e}")  # Replace with proper logging in production
                    raise HTTPException(
                        status_code=500,
                        detail="An error occurred while parsing the document."
                    )

        def __summarize_text(text, max_length=512, summary_max_length=150, summary_min_length=25):
            """
            Summarize the text if its tokenized length is within the model's maximum limit.

            Args:
                text (str): The input text to summarize.
                max_length (int): The maximum token length allowed for the model.
                summary_max_length (int): Maximum length of the summary.
                summary_min_length (int): Minimum length of the summary.

            Returns:
                str or None: The summary if tokenized text is within max_length; None otherwise.
            """
            tokens = self.tokenizer(text, return_tensors="pt", truncation=False)
            num_tokens = len(tokens["input_ids"][0])

            if num_tokens >= max_length:
                summary = self.summarizer(
                    text, max_length=summary_max_length, min_length=summary_min_length, do_sample=False
                )
                return summary[0]["summary_text"]
            else:
                return ''