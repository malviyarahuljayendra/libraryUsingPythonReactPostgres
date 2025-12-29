import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database.infrastructure.models.base import Base

class LoanModel(Base):
    __tablename__ = "loans"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    copy_id = Column(String, ForeignKey("book_copies.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(String, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)

    # Relationships
    copy = relationship("BookCopyModel", back_populates="loans")
    member = relationship("MemberModel", back_populates="loans")
