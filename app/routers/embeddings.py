from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post("/embeddings/create")
def create_embedding(embeddings: List[float]):
    return {"message": "Create embedding"}


@router.get("/embeddings/{embedding_id}")
def get_embedding(embedding_id: str):
    return {"message": f"Get embedding with id {embedding_id}"}


@router.post("/embeddings/{embedding_id}/update")
def update_embedding(embedding_id: str):
    return {"message": f"Update embedding with id {embedding_id}"}


@router.delete("/embeddings/{embedding_id}/delete")
def delete_embedding(embedding_id: str):
    return {"message": f"Delete embedding with id {embedding_id}"}


@router.get("/embeddings/{embedding_id}/similar")
def get_similar_embeddings(embedding_id: str):
    return {"message": f"Get similar embeddings for embedding with id {embedding_id}"}
