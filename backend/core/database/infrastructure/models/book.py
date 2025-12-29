import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database.infrastructure.models.base import Base
from backend.core.database.infrastructure.models.genre import book_genre

class BookMetadataModel(Base):
    __tablename__ = "books_metadata"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    
    author_id = Column(String, ForeignKey("authors.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    author = relationship("AuthorModel", back_populates="books")
    genres = relationship("GenreModel", secondary=book_genre, back_populates="books")
    copies = relationship("BookCopyModel", back_populates="metadata_rec", cascade="all, delete-orphan")

class BookCopyModel(Base):
    __tablename__ = "book_copies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    book_metadata_id = Column(String, ForeignKey("books_metadata.id", ondelete="CASCADE"), nullable=False)
    is_available = Column(Boolean, default=True)
    status = Column(String, default="Available")

    # Relationship back to metadata
    metadata_rec = relationship("BookMetadataModel", back_populates="copies")
    loans = relationship("LoanModel", back_populates="copy")
