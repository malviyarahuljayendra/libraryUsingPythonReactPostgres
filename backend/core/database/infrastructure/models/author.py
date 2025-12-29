import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from backend.core.database.infrastructure.models.base import Base

class AuthorModel(Base):
    __tablename__ = "authors"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    bio = Column(Text, nullable=True)

    # Relationship to books
    books = relationship("BookMetadataModel", back_populates="author")
