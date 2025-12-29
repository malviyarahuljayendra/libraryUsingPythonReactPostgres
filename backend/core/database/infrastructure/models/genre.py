import uuid
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database.infrastructure.models.base import Base

# Association table for many-to-many relationship
book_genre = Table(
    "book_genre",
    Base.metadata,
    Column("book_id", String, ForeignKey("books_metadata.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", String, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
)

class GenreModel(Base):
    __tablename__ = "genres"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)

    # Relationship to books (many-to-many)
    books = relationship("BookMetadataModel", secondary=book_genre, back_populates="genres")
