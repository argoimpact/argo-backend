from typing import List, Union
from pydantic import BaseModel


class GenerateAndUpsertEmbeddingRequest(BaseModel):
    text: Union[str, List[str]]
    index: str
    namespace: str
