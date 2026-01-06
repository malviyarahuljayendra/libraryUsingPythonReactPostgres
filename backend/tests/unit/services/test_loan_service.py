import pytest
from unittest.mock import MagicMock
from datetime import datetime
from backend.services.loan_service import LoanService
from backend.core.database import LoanModel, BookCopyModel
from backend.core.exceptions import ValidationError, EntityNotFoundError

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def loan_service(mock_session):
    return LoanService(mock_session, validators=[])

def test_borrow_book_success(loan_service, mock_session):
    mock_copy = BookCopyModel(id="copy123", is_available=True)
    loan_service.book_repo.get_available_copy = MagicMock(return_value=mock_copy)
    
    loan = loan_service.borrow_book(book_id="book1", member_id="mem1")
    
    assert loan.copy_id == "copy123"
    assert loan.member_id == "mem1"
    assert not mock_copy.is_available
    assert mock_copy.status == "Borrowed"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_borrow_book_with_copy_id_success(loan_service, mock_session):
    mock_copy = BookCopyModel(id="copy123", is_available=True)
    loan_service.book_repo.get_copy_by_id = MagicMock(return_value=mock_copy)
    
    loan = loan_service.borrow_book(book_id="book1", member_id="mem1", copy_id="copy123")
    
    assert loan.copy_id == "copy123"
    assert not mock_copy.is_available
    loan_service.book_repo.get_copy_by_id.assert_called_with("copy123")

def test_borrow_book_no_available_copies(loan_service):
    loan_service.book_repo.get_available_copy = MagicMock(return_value=None)
    
    with pytest.raises(ValidationError) as exc:
        loan_service.borrow_book(book_id="book1", member_id="mem1")
    assert "No available copies" in str(exc.value)

def test_borrow_book_copy_not_available(loan_service):
    mock_copy = BookCopyModel(id="copy123", is_available=False)
    loan_service.book_repo.get_copy_by_id = MagicMock(return_value=mock_copy)
    
    with pytest.raises(ValidationError) as exc:
        loan_service.borrow_book(book_id="book1", member_id="mem1", copy_id="copy123")
    assert "Requested copy is not available" in str(exc.value)

def test_return_book_success(loan_service, mock_session):
    mock_loan = LoanModel(id="loan1", copy_id="copy1", returned_at=None)
    mock_copy = BookCopyModel(id="copy1", is_available=False)
    
    loan_service.loan_repo.get_by_id = MagicMock(return_value=mock_loan)
    loan_service.book_repo.get_copy_by_id = MagicMock(return_value=mock_copy)
    
    returned_loan = loan_service.return_book("loan1")
    
    assert returned_loan.returned_at is not None
    assert mock_copy.is_available
    assert mock_copy.status == "Available"
    mock_session.commit.assert_called_once()

def test_return_book_not_found(loan_service):
    loan_service.loan_repo.get_by_id = MagicMock(return_value=None)
    
    with pytest.raises(EntityNotFoundError) as exc:
        loan_service.return_book("999")
    assert "Loan record not found" in str(exc.value)

def test_return_already_returned_book(loan_service):
    mock_loan = LoanModel(id="loan1", returned_at=datetime.utcnow())
    loan_service.loan_repo.get_by_id = MagicMock(return_value=mock_loan)
    
    with pytest.raises(ValidationError) as exc:
        loan_service.return_book("loan1")
    assert "already returned" in str(exc.value)

def test_list_member_loans(loan_service):
    mock_items = [LoanModel(id="l1"), LoanModel(id="l2")]
    loan_service.loan_repo.paginated_list_by_member = MagicMock(return_value=(mock_items, 2))
    
    result = loan_service.list_member_loans(member_id="mem1", page=1, limit=10)
    
    assert len(result['loans']) == 2
    assert result['total_count'] == 2
    assert result['total_pages'] == 1
