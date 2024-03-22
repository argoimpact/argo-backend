from pydantic import BaseModel


class RFP(BaseModel):
    id: str
    title: str
    description: str
    user_id: str
