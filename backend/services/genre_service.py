from sqlalchemy.orm import Session
from backend.core.database import GenreRepository, GenreModel
from backend.core.exceptions import ValidationError
from backend.core.constants import Limits
from backend.core.messages import ErrorMessages
from backend.core.utils import build_paginated_response

class GenreService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = GenreRepository(session)

    def create_genre(self, name: str) -> GenreModel:
        if not name or not name.strip():
            raise ValidationError(ErrorMessages.GENRE_NAME_REQUIRED)
        if len(name) > Limits.GENRE_NAME_MAX:
             raise ValidationError(ErrorMessages.GENRE_NAME_TOO_LONG.format(max=Limits.GENRE_NAME_MAX))
        existing = self.session.query(GenreModel).filter_by(name=name).first()
        if existing:
            # User Request: Validate and prevent same name addition
            raise ValidationError(f"Genre with name '{name}' already exists.")
            
        genre = GenreModel(name=name)
        self.repo.add(genre)
        self.session.flush()
        self.session.refresh(genre)
        return genre

    def list_genres(self, page: int = 1, limit: int = 10) -> dict:
        items, total_count = self.repo.paginated_list(page, limit)
        return build_paginated_response(items, total_count, limit, "genres")
