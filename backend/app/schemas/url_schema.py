from pydantic import BaseModel, HttpUrl

class url_s(BaseModel):
    url:HttpUrl
