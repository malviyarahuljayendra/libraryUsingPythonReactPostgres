from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Tuple
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.core.database.infrastructure.models import (
    BookMetadataModel, BookCopyModel, MemberModel, LoanModel, AuthorModel, GenreModel
)
from sqlalchemy.exc import IntegrityError, OperationalError
from backend.core.exceptions import ConflictError, DatabaseError

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    def list_all(self) -> List[T]:
        pass

    def paginated_list(self, page: int = 1, limit: int = 10) -> Tuple[List[T], int]:
        # Default implementation if T is mapped to a table
        pass



class AuthorRepository(IRepository[AuthorModel]):
    def add(self, author: AuthorModel) -> AuthorModel:
        self.session.add(author)
        return author

    def get_by_id(self, id: str) -> Optional[AuthorModel]:
        return self.session.query(AuthorModel).filter_by(id=id).first()

    def list_all(self) -> List[AuthorModel]:
        return self.session.query(AuthorModel).all()

    def paginated_list(self, page: int = 1, limit: int = 10) -> Tuple[List[AuthorModel], int]:
        query = self.session.query(AuthorModel)
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return items, total

class GenreRepository(IRepository[GenreModel]):
    def add(self, genre: GenreModel) -> GenreModel:
        self.session.add(genre)
        return genre

    def get_by_id(self, id: str) -> Optional[GenreModel]:
        return self.session.query(GenreModel).filter_by(id=id).first()

    def list_all(self) -> List[GenreModel]:
        return self.session.query(GenreModel).all()

    def paginated_list(self, page: int = 1, limit: int = 10) -> Tuple[List[GenreModel], int]:
        query = self.session.query(GenreModel)
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return items, total

    def list_by_ids(self, ids: List[str]) -> List[GenreModel]:
        return self.session.query(GenreModel).filter(GenreModel.id.in_(ids)).all()

class BookRepository(IRepository[BookMetadataModel]):
    def add(self, book: BookMetadataModel) -> BookMetadataModel:
        self.session.add(book)
        return book

    def get_by_id(self, id: str) -> Optional[BookMetadataModel]:
        return self.session.query(BookMetadataModel).filter_by(id=id).first()

    def get_by_isbn(self, isbn: str) -> Optional[BookMetadataModel]:
        return self.session.query(BookMetadataModel).filter_by(isbn=isbn).first()

    def list_all(self) -> List[BookMetadataModel]:
        return self.session.query(BookMetadataModel).all()

    def paginated_list(self, page: int = 1, limit: int = 10) -> Tuple[List[BookMetadataModel], int]:
        query = self.session.query(BookMetadataModel)
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return items, total

    def add_copy(self, copy: BookCopyModel) -> BookCopyModel:
        self.session.add(copy)
        return copy

    def get_copy_by_id(self, copy_id: str) -> Optional[BookCopyModel]:
        return self.session.query(BookCopyModel).filter_by(id=copy_id).first()

    def get_available_copy(self, book_id: str) -> Optional[BookCopyModel]:
        return self.session.query(BookCopyModel).filter_by(
            book_metadata_id=book_id, is_available=True
        ).first()

    def paginated_list_copies(self, book_id: str, page: int = 1, limit: int = 10) -> Tuple[List[BookCopyModel], int]:
        query = self.session.query(BookCopyModel).filter_by(book_metadata_id=book_id)
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return items, total

class MemberRepository(IRepository[MemberModel]):
    def add(self, member: MemberModel) -> MemberModel:
        self.session.add(member)
        return member

    def get_by_id(self, id: str) -> Optional[MemberModel]:
        return self.session.query(MemberModel).filter_by(id=id).first()

    def get_by_email(self, email: str) -> Optional[MemberModel]:
        return self.session.query(MemberModel).filter_by(email=email).first()

    def list_all(self) -> List[MemberModel]:
        return self.session.query(MemberModel).all()

    def paginated_list(self, page: int = 1, limit: int = 10) -> Tuple[List[MemberModel], int]:
        query = self.session.query(MemberModel)
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return items, total

class LoanRepository(IRepository[LoanModel]):
    def add(self, loan: LoanModel) -> LoanModel:
        self.session.add(loan)
        return loan

    def get_by_id(self, id: str) -> Optional[LoanModel]:
        return self.session.query(LoanModel).filter_by(id=id).first()

    def list_all(self) -> List[LoanModel]:
        return self.session.query(LoanModel).all()

    def list_by_member(self, member_id: str) -> List[LoanModel]:
        return self.session.query(LoanModel).filter_by(member_id=member_id).all()

    def paginated_list_by_member(self, member_id: Optional[str], page: int = 1, limit: int = 10) -> Tuple[List[LoanModel], int]:
        query = self.session.query(LoanModel)
        if member_id:
            query = query.filter_by(member_id=member_id)
        
        # Order by borrowed_at desc
        query = query.order_by(LoanModel.borrowed_at.desc())
        
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return items, total
