import logging
from typing import List, Union
import openai
from pydantic import BaseModel, Field
from pinecone import Pinecone

from app.config import app_config

from app.models.vectordb import Vector

logger = logging.getLogger(__name__)


class Embedding(BaseModel):
    index: int
    embedding: List[float]
    object: str = "embedding"


class EmbeddingResponse(BaseModel):
    embeddings: List[Embedding] = Field(
        ..., title="List of embeddings from openai response"
    )


class EmbeddingRequest(BaseModel):
    text: Union[str, List[str]]
    model: str


def generate_embedding(
    request: EmbeddingRequest, client: openai.Client
) -> EmbeddingResponse:
    text = request.text
    logger.info(f"Generating embeddings for text: {text}")
    response = client.embeddings.create(input=text, model=request.model)
    data = response.data

    embeddings = [Embedding(**dict(embedding)) for embedding in data]
    return EmbeddingResponse(embeddings=embeddings)


class UpsertRequest(BaseModel):
    vectors: List[Vector]
    index: str
    namespace: str


def upsert_embedding(request: UpsertRequest, client: Pinecone) -> int:
    try:
        logger.info(f"Upserting embeddings to index: {request.index}")
        index = client.Index(host=app_config.pinecone_index_host)
        response = index.upsert(
            vectors=[v.model_dump() for v in request.vectors],
            namespace=request.namespace,
        )

        return response.upserted_count
    except Exception as e:
        logger.error(f"Error upserting embeddings: {e}")
        raise
