from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from backend.core.database import (
    BookRepository, MemberRepository, LoanRepository, AuthorRepository, GenreRepository,
    BookMetadataModel, BookCopyModel, MemberModel, LoanModel, AuthorModel, GenreModel
)
from backend.services.validators import ILoanValidator
from backend.core.exceptions import ConflictError, EntityNotFoundError, ValidationError

class AuthorManager:
    def __init__(self, session: Session):
        self.session = session
        self.repo = AuthorRepository(session)

    def create_author(self, name: str, bio: str = None) -> AuthorModel:
        existing = self.session.query(AuthorModel).filter_by(name=name).first()
        if existing:
            return existing
            
        author = AuthorModel(name=name, bio=bio)
        self.repo.add(author)
        self.session.commit()
        self.session.refresh(author)
        return author

    def list_authors(self) -> List[AuthorModel]:
        return self.repo.list_all()

class GenreManager:
    def __init__(self, session: Session):
        self.session = session
        self.repo = GenreRepository(session)

    def create_genre(self, name: str) -> GenreModel:
        existing = self.session.query(GenreModel).filter_by(name=name).first()
        if existing:
            return existing
            
        genre = GenreModel(name=name)
        self.repo.add(genre)
        self.session.commit()
        self.session.refresh(genre)
        return genre

    def list_genres(self) -> List[GenreModel]:
        return self.repo.list_all()

class BookManager:
    def __init__(self, session: Session):
        self.session = session
        self.repo = BookRepository(session)
        self.genre_repo = GenreRepository(session)

    def create_book(self, title: str, isbn: str, author_id: str = None, genre_ids: List[str] = None, initial_copies: int = 0) -> BookMetadataModel:
        print(f"Creating book: {title}, ISBN: {isbn}, Initial Copies: {initial_copies}")
        if self.repo.get_by_isbn(isbn):
            raise ConflictError("Book with this ISBN already exists")
        
        book = BookMetadataModel(title=title, isbn=isbn, author_id=author_id)
        
        if genre_ids:
            genres = self.genre_repo.list_by_ids(genre_ids)
            book.genres = genres
            
        self.repo.add(book)
        
        for _ in range(initial_copies):
            copy = BookCopyModel()
            book.copies.append(copy)
            
        self.session.commit()
        self.session.refresh(book)
        print(f"Book created. Total copies in model: {len(book.copies)}")
        return book

    def list_books(self) -> List[BookMetadataModel]:
        return self.repo.list_all()

    def update_book(self, book_id: str, title: str = None, isbn: str = None, author_id: str = None, genre_ids: List[str] = None) -> BookMetadataModel:
        book = self.repo.get_by_id(book_id)
        if not book:
            raise EntityNotFoundError("Book not found")
        
        if title is not None: book.title = title
        if author_id is not None: book.author_id = author_id
        if isbn is not None:
            if isbn != book.isbn and self.repo.get_by_isbn(isbn):
                raise ConflictError("Book with this ISBN already exists")
            book.isbn = isbn
        
        if genre_ids is not None:
            genres = self.genre_repo.list_by_ids(genre_ids)
            book.genres = genres
            
        self.session.commit()
        self.session.refresh(book)
        return book

    def add_copy(self, book_id: str) -> BookCopyModel:
        book = self.repo.get_by_id(book_id)
        if not book:
            raise EntityNotFoundError("Book not found")
        
        copy = BookCopyModel(book_metadata_id=book_id)
        self.repo.add_copy(copy)
        self.session.commit()
        self.session.refresh(copy)
        return copy

    def list_copies(self, book_id: str) -> List[BookCopyModel]:
        book = self.repo.get_by_id(book_id)
        if not book:
            raise EntityNotFoundError("Book not found")
        return book.copies

class MemberManager:
    def __init__(self, session: Session):
        self.session = session
        self.repo = MemberRepository(session)

    def create_member(self, name: str, email: str) -> MemberModel:
        if self.repo.get_by_email(email):
            raise ConflictError("Member with this email already exists")
            
        member = MemberModel(name=name, email=email)
        self.repo.add(member)
        self.session.commit()
        self.session.refresh(member)
        return member

    def list_members(self) -> List[MemberModel]:
        return self.repo.list_all()

    def update_member(self, member_id: str, name: str = None, email: str = None) -> MemberModel:
        member = self.repo.get_by_id(member_id)
        if not member:
            raise EntityNotFoundError("Member not found")
            
        if name is not None: member.name = name
        if email is not None:
            if email != member.email and self.repo.get_by_email(email):
                raise ConflictError("Member with this email already exists")
            member.email = email
            
        self.session.commit()
        self.session.refresh(member)
        return member

class LoanManager:
    def __init__(self, session: Session, validators: List[ILoanValidator]):
        self.session = session
        self.validators = validators
        self.loan_repo = LoanRepository(session)
        self.book_repo = BookRepository(session)
        self.member_repo = MemberRepository(session)

    def borrow_book(self, book_id: str, member_id: str, copy_id: str = None) -> LoanModel:
        # Run all validators
        for validator in self.validators:
            validator.validate(book_id, member_id, self.book_repo, self.member_repo)

        # Proceed
        if copy_id:
            copy = self.book_repo.get_copy_by_id(copy_id)
            if not copy or not copy.is_available:
                raise ValidationError("Requested copy is not available")
        else:
            copy = self.book_repo.get_available_copy(book_id)
            if not copy:
                raise ValidationError("No available copies for this book")

        loan = LoanModel(
            copy_id=copy.id, 
            member_id=member_id, 
            borrowed_at=datetime.utcnow()
        )
        copy.is_available = False
        copy.status = "Borrowed"
        
        self.loan_repo.add(loan)
        
        self.session.commit()
        self.session.refresh(loan)
        return loan

    def return_book(self, loan_id: str) -> LoanModel:
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            raise EntityNotFoundError("Loan record not found")
        
        if loan.returned_at:
            raise ValidationError("Book already returned")

        copy = self.book_repo.get_copy_by_id(loan.copy_id)
        
        loan.returned_at = datetime.utcnow()
        if copy:
            copy.is_available = True
            copy.status = "Available"
        
        self.session.commit()
        self.session.refresh(loan)
        return loan

    def list_member_loans(self, member_id: str) -> List[LoanModel]:
        return self.loan_repo.list_by_member(member_id)
