from pydantic import BaseModel


class RFPBase(BaseModel):
    title: str
    description: str


class RFPCreate(RFPBase):
    pass


class RFPUpdate(RFPBase):
    pass
