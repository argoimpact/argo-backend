from typing import List
from pydantic import BaseModel

# TODO: here is where we define our vector database models, schema, and metadata


class VectorMetaData(BaseModel):
    text: str
    title: str


class Vector(BaseModel):
    id: str
    values: List[float]
    metadata: VectorMetaData
