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
    username: str | None = None
    email: str | None = None
    password: str | None = None

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
    filename: str | None = None
    filename: str | None = None
    raw_text: str | None = None
    corrected_html: str | None = None
    
    # New: Tags
    tags: list["TagResponse"] = []

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
