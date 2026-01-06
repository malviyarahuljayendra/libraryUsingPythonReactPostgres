from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from backend.core.database import LoanRepository, BookRepository, MemberRepository, LoanModel
from backend.services.validators import ILoanValidator
from backend.core.exceptions import ValidationError, EntityNotFoundError

class LoanService:
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
        
        self.session.flush()
        self.session.refresh(loan)
        return loan

    def return_book(self, loan_id: str) -> LoanModel:
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            raise EntityNotFoundError("Loan record not found")
        
        if loan.returned_at:
            raise ValidationError("Book already returned")

        copy = self.book_repo.get_copy_by_id(loan.copy_id)
        
        if copy:
            copy.is_available = True
            copy.status = "Available"
        
        # User Requirement: Do not keep member's return activity in db
        self.session.delete(loan)
        self.session.flush()
        
        # Note: loan object is now detached/expired, but we return it for ID reference if needed
        # We manually set returned_at for the response logic before it vanishes
        loan.returned_at = datetime.utcnow() 
        return loan

    def list_member_loans(self, member_id: str = None, page: int = 1, limit: int = 10) -> dict:
        items, total_count = self.loan_repo.paginated_list_by_member(member_id, page, limit)
        total_pages = (total_count + limit - 1) // limit if limit > 0 else 0
        return {
            "loans": items,
            "total_count": total_count,
            "total_pages": total_pages
        }

    def list_all_loans(self, page: int = 1, limit: int = 10) -> dict:
        """List all loans in the system (no member filter)"""
        return self.list_member_loans(member_id=None, page=page, limit=limit)
