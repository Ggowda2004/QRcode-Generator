from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class VcardRequest(BaseModel):
    # Required fields
    first_name: str
    last_name: str
    
    # Optional contact fields
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    
    # Optional personal info
    organization: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    
    # Optional address fields
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    
    # Optional additional info
    note: Optional[str] = None
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format"""
        if v is not None:
            # Remove non-digit characters except + and -
            cleaned = ''.join(c for c in v if c.isdigit() or c in ['+', '-'])
            if not cleaned:
                raise ValueError('Phone number must contain digits')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone": "+1-555-0123",
                "organization": "Acme Corp",
                "title": "Software Engineer",
                "url": "https://johndoe.com",
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "country": "USA",
                "note": "Available for consulting"
            }
        }
