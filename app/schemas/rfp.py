from pydantic import BaseModel
from fastapi import UploadFile, File


class RFPBase(BaseModel):
    title: str
    description: str


class RFPCreate(RFPBase):
    file: UploadFile = File(...)
    pass


class RFPUpdate(RFPBase):
    pass


class RFPResponse(RFPBase):
    id: str
    user_id: str
    file_id: str
