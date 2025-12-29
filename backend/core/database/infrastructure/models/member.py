from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class MemberModel(Base):
    __tablename__ = "members"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Relationships
    loans = relationship("LoanModel", back_populates="member")
