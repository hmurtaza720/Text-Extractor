from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    security_code: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class DocumentCreate(BaseModel):
    pass # Upload is handled via Form data (UploadFile)

class DocumentResponse(BaseModel):
    id: int
    user_id: int
    upload_date: str
    status: str
    original_path: str
    filename: Optional[str] = None
    raw_text: Optional[str] = None
    corrected_html: Optional[str] = None
    
    # New: Tags
    tags: List["TagResponse"] = []

    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str
    color: str = "blue"

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    
    class Config:
        from_attributes = True
