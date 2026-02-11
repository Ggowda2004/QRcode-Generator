from pydantic import BaseModel,EmailStr

class mail_s(BaseModel):
    url:EmailStr