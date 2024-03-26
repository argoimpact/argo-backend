from typing import List, Union
import openai
from app.config import app_config
from app.dependencies import get_openai_client
from app.utils.embeddings import generate_embedding, EmbeddingRequest, EmbeddingResponse
from fastapi import APIRouter, Depends, HTTPException, status


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
