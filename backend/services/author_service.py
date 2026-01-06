from sqlalchemy.orm import Session
from backend.core.database import AuthorRepository, AuthorModel
from backend.core.exceptions import ValidationError
from backend.core.constants import Limits
from backend.core.messages import ErrorMessages
from backend.core.utils import build_paginated_response

class AuthorService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = AuthorRepository(session)

    def create_author(self, name: str, bio: str = None) -> AuthorModel:
        if not name or not name.strip():
            raise ValidationError(ErrorMessages.AUTHOR_NAME_REQUIRED)
        if len(name) > Limits.AUTHOR_NAME_MAX:
            raise ValidationError(ErrorMessages.AUTHOR_NAME_TOO_LONG.format(max=Limits.AUTHOR_NAME_MAX))
        existing = self.session.query(AuthorModel).filter_by(name=name).first()
        if existing:
            # User Request: Validate and prevent same name addition
            raise ValidationError(f"Author with name '{name}' already exists.")
            
        author = AuthorModel(name=name, bio=bio)
        self.repo.add(author)
        self.session.flush()
        self.session.refresh(author)
        return author

    def list_authors(self, page: int = 1, limit: int = 10) -> dict:
        items, total_count = self.repo.paginated_list(page, limit)
        return build_paginated_response(items, total_count, limit, "authors")
