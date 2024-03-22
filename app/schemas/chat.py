from pydantic import BaseModel


class ChatMessageCreate(BaseModel):
    content: str
