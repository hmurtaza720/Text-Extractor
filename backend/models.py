from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True) # Used as Full Name in frontend, distinct from email
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # Foreign Key relationship handled logically or via ForeignKey constraint if preferred
    # For strictness: user_id = Column(Integer, ForeignKey("users.id")) setting up relationship
    # keeping simple for now, but adding relationship back ref is good practice
    
    upload_date = Column(String(50)) # Using string for simplicity, or DateTime
    original_path = Column(String(255))
    filename = Column(String(255)) # Display name of the file
    raw_text = Column(String(5000)) # Large text field (TEXT in mysql)
    corrected_html = Column(String(5000)) # Large text field
    status = Column(String(20), default="Processing") # Processing, Ready, Error

class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True) # FK to documents.id
    version_number = Column(Integer)
    corrected_html = Column(String(5000))
    timestamp = Column(String(50))

# Association Table for Many-to-Many
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship

document_tags = Table('document_tags', Base.metadata,
    Column('document_id', Integer, ForeignKey('documents.id', ondelete="CASCADE")),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete="CASCADE"))
)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    color = Column(String(20), default="blue") # e.g., 'blue', 'red', 'green'

    # Relationship
    documents = relationship("Document", secondary=document_tags, back_populates="tags")

# Update Document to include tags relationship
Document.tags = relationship("Tag", secondary=document_tags, back_populates="documents")
