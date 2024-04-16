import logging
from typing import List, Union
from pydantic import BaseModel

from langchain_text_splitters import RecursiveCharacterTextSplitter 
from pdfminer.high_level import extract_text
from app.config import app_config

logger = logging.getLogger(__name__)

class DocPath(BaseModel):
    doc_path: str
    object: str = "document file path"

class DocText(BaseModel):
    text: str
    object: str = "document's text"


def generate_text_from_path(
    request: DocPath
) -> DocText:
    doc_path = request.doc_path
    logger.info(f"Generating text for file: {doc_path}")
    text = extract_text(doc_path)

    return DocText(text=text)

class Chunks(BaseModel):
    texts: Union[str, List[str]]
    object: str = "chunks"

def generate_chunks(
    request: DocText, 
    chunk_size: int = 4000,
    chunk_overlap: int = 200
) -> Chunks:
    text = request.text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    logger.info(f"Generating chunks")
    langchain_texts = text_splitter.create_documents([text])
    texts = []
    for txt in langchain_texts:
        texts.append(txt.page_content)
    
    return Chunks(texts=texts)




