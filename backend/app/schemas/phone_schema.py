from pydantic import BaseModel

class PhoneRequest(BaseModel):
    number: str