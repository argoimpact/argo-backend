from typing import List, Union
import openai
from pydantic import BaseModel, Field


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
    response = client.embeddings.create(input=text, model=request.model)
    data = response.data

    embeddings = [Embedding(**dict(embedding)) for embedding in data]
    return EmbeddingResponse(embeddings=embeddings)
