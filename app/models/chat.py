from pydantic import BaseModel
from datetime import datetime
from typing import List


class ChatMessage(BaseModel):
    id: str
    user_id: str
    content: str
    timestamp: datetime


class ChatHistory(BaseModel):
    user_id: str
    messages: List[ChatMessage]

    @classmethod
    async def get_history(cls, user_id: str):
        # Logic to retrieve chat history from the database
        # Example:
        # db_messages = await ChatMessage.find(user_id=user_id).sort("-timestamp").to_list()
        # return cls(user_id=user_id, messages=db_messages)
        pass
