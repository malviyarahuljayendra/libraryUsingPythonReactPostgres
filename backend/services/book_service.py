from typing import List
from sqlalchemy.orm import Session
from backend.core.database import BookRepository, GenreRepository, BookMetadataModel, BookCopyModel
from backend.core.exceptions import ValidationError, ConflictError, EntityNotFoundError
from backend.core.logger import logger
from backend.core.constants import Limits
from backend.core.messages import ErrorMessages
from backend.core.utils import build_paginated_response

class BookService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = BookRepository(session)
        self.genre_repo = GenreRepository(session)

    def create_book(self, title: str, isbn: str, author_id: str = None, genre_ids: List[str] = None, initial_copies: int = 0) -> BookMetadataModel:
        logger.info(f"Creating book: {title}, ISBN: {isbn}, Initial Copies: {initial_copies}")
        if not title or not title.strip():
            raise ValidationError(ErrorMessages.BOOK_TITLE_REQUIRED)
        if len(title) > Limits.BOOK_TITLE_MAX:
            raise ValidationError(ErrorMessages.BOOK_TITLE_TOO_LONG.format(max=Limits.BOOK_TITLE_MAX))
        if initial_copies < 0:
            raise ValidationError(ErrorMessages.BOOK_COPIES_NEGATIVE)
            
        if not isbn:
            raise ValidationError(ErrorMessages.BOOK_ISBN_REQUIRED)
        # Basic ISBN length check (stripping hyphens)
        clean_isbn = isbn.replace("-", "").replace(" ", "")
        if len(clean_isbn) not in [10, 13]:
             raise ValidationError(f"{ErrorMessages.BOOK_ISBN_INVALID} (Received {len(clean_isbn)} digits)")
             
        if self.repo.get_by_isbn(isbn):
            raise ConflictError(ErrorMessages.BOOK_ISBN_EXISTS)
        
        book = BookMetadataModel(title=title, isbn=isbn, author_id=author_id)
        
        if genre_ids:
            genres = self.genre_repo.list_by_ids(genre_ids)
            book.genres = genres
            
        self.repo.add(book)
        
        for _ in range(initial_copies):
            copy = BookCopyModel()
            book.copies.append(copy)
            
            book.copies.append(copy)
            
        self.session.flush()
        self.session.refresh(book)
        logger.info(f"Book created. Total copies in model: {len(book.copies)}")
        return book

    def list_books(self, page: int = 1, limit: int = 10) -> dict:
        items, total_count = self.repo.paginated_list(page, limit)
        return build_paginated_response(items, total_count, limit, "books")

    def update_book(self, book_id: str, title: str = None, isbn: str = None, author_id: str = None, genre_ids: List[str] = None) -> BookMetadataModel:
        book = self.repo.get_by_id(book_id)
        if not book:
            raise EntityNotFoundError("Book not found")
        
        if title is not None: book.title = title
        if author_id is not None: book.author_id = author_id
        if isbn is not None:
            if isbn != book.isbn and self.repo.get_by_isbn(isbn):
                raise ConflictError(ErrorMessages.BOOK_ISBN_EXISTS)
            book.isbn = isbn
        
        if genre_ids is not None:
            genres = self.genre_repo.list_by_ids(genre_ids)
            book.genres = genres
            
            
        self.session.flush()
        self.session.refresh(book)
        return book

    def add_copy(self, book_id: str) -> BookCopyModel:
        book = self.repo.get_by_id(book_id)
        if not book:
            raise EntityNotFoundError("Book not found")
        
        copy = BookCopyModel(book_metadata_id=book_id)
        self.repo.add_copy(copy)
        self.repo.add_copy(copy)
        self.session.flush()
        self.session.refresh(copy)
        return copy

    def list_copies(self, book_id: str, page: int = 1, limit: int = 10) -> dict:
        items, total_count = self.repo.paginated_list_copies(book_id, page, limit)
        return build_paginated_response(items, total_count, limit, "copies")
