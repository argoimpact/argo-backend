import logging
from typing import List, Union
import openai
from pinecone import Pinecone
from app.config import app_config
from app.dependencies import get_openai_client, get_pinecone_client
from app.models.vectordb import Vector, VectorMetaData

from app.schemas.embeddings import GenerateAndUpsertEmbeddingRequest
from app.utils.embeddings import (
    UpsertRequest,
    upsert_embedding,
    generate_embedding,
    EmbeddingRequest,
    EmbeddingResponse,
)
from fastapi import APIRouter, Depends, HTTPException, status


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate")
def create_embedding(
    text: Union[str, List[str]],
    openai_client: openai.Client = Depends(get_openai_client),
):
    request = EmbeddingRequest(text=text, model=app_config.embedding_model_ada)
    response: EmbeddingResponse = generate_embedding(request, openai_client)

    # upsert to database
    return {"message": dict(response)}


@router.post("/upsert")
def generate_and_upsert_embedding(
    upsert_request: GenerateAndUpsertEmbeddingRequest,
    openai_client: openai.Client = Depends(get_openai_client),
    pinecone_client: Pinecone = Depends(get_pinecone_client),
):
    """creates and upserts embeddings to the database"""
    text = upsert_request.text
    namespace = upsert_request.namespace
    index = upsert_request.index

    # generate embedding from text
    logger.info(f"Generating embeddings for text: {text}")
    request = EmbeddingRequest(text=text, model=app_config.embedding_model_ada)
    response: EmbeddingResponse = generate_embedding(request, openai_client)

    # check to see if text is a list or string
    if isinstance(text, str):
        text = [text]

    # create vectors
    vectors = [
        Vector(
            id=f"text-{idx}",
            values=embedding.embedding,
            metadata=VectorMetaData(text=text[idx]),
        )
        for idx, embedding in enumerate(response.embeddings)
    ]
    logger.info("im hereer")

    upsert_request = UpsertRequest(vectors=vectors, index=index, namespace=namespace)
    logger.info(f"Upserting embeddings to index: {index} with request {upsert_request}")
    upsert_response = upsert_embedding(upsert_request, pinecone_client)
    logger.info(f"Upsert response: {upsert_response}")
    return {"upsert response": upsert_response}

    # upsert to database
