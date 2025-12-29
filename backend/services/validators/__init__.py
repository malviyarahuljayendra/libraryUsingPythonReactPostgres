from abc import ABC, abstractmethod
from backend.core.database import BookRepository, MemberRepository, BookMetadataModel, MemberModel
from backend.core.exceptions import EntityNotFoundError, ValidationError

class ILoanValidator(ABC):
    @abstractmethod
    def validate(self, book_id: str, member_id: str, book_repo: BookRepository, member_repo: MemberRepository) -> None:
        """
        Validates if a loan can proceed. Raises LibraryError if validation fails.
        """
        pass

class BookAvailabilityValidator(ILoanValidator):
    def validate(self, book_id: str, member_id: str, book_repo: BookRepository, member_repo: MemberRepository) -> None:
        book = book_repo.get_by_id(book_id)
        if not book:
            raise EntityNotFoundError("Book not found")
        
        available_copy = book_repo.get_available_copy(book_id)
        if not available_copy:
            raise ValidationError("Book is not available (no copies left)")

class MemberExistenceValidator(ILoanValidator):
    def validate(self, book_id: str, member_id: str, book_repo: BookRepository, member_repo: MemberRepository) -> None:
        member = member_repo.get_by_id(member_id)
        if not member:
            raise EntityNotFoundError("Member not found")
