import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from backend.core.database.infrastructure.models.base import Base

from backend.core.database.infrastructure.models.base import Base
from backend.core.constants import DBTables
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
import uuid

class AuthorModel(Base):
    __tablename__ = DBTables.AUTHORS # "authors"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    bio = Column(Text, nullable=True)

    # Relationship to books
    books = relationship("BookMetadataModel", back_populates="author")
