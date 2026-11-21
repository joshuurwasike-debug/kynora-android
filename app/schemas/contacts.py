from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=30)
    company: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=2000)


class ContactResponse(BaseModel):
    id: int
    workspace_id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None
    created_at: str
    updated_at: str
class ContactUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=30)
    company: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=2000)
