from unittest.mock import MagicMock, patch
import pytest
from datetime import datetime

from backend.api.service import LibraryService
from backend.generated import library_pb2
from backend.core.database import BookCopyModel, BookMetadataModel

class TestLoanService:
    @pytest.fixture
    def mock_db_scope(self):
        with patch('backend.api.service.db_scope') as mock:
            yield mock

    @pytest.fixture
    def service(self):
        return LibraryService()

    def test_list_all_loans(self, service, mock_db_scope):
        # Mock DB setup
        mock_db = MagicMock()
        mock_db_scope.return_value.__enter__.return_value = mock_db
        
        # Mock Loan Service
        with patch('backend.api.service.LoanService') as MockLoanService:
            mock_loan_service = MockLoanService.return_value
            
            # Mock Data
            mock_loan = MagicMock()
            mock_loan.id = "loan1"
            mock_loan.copy_id = "copy1"
            mock_loan.member_id = "member1"
            mock_loan.borrowed_at = datetime(2023, 1, 1)
            mock_loan.returned_at = None
            
            # Mock Relationships
            mock_loan.copy.metadata_rec.title = "Test Book"
            mock_loan.member.name = "Member Name"
            mock_loan.member.email = "Member Email"
            
            mock_loan_service.list_all_loans.return_value = {
                'loans': [mock_loan],
                'total_count': 1,
                'total_pages': 1
            }
            
            # Request
            request = library_pb2.ListAllLoansRequest(page=1, limit=10)
            response = service.ListAllLoans(request, None)
            
            # Assertions
            assert len(response.loans) == 1
            assert response.loans[0].id == "loan1"
            assert response.loans[0].book_title == "Test Book"
            assert response.loans[0].member_name == "Member Name"
            assert response.loans[0].member_email == "Member Email"
            assert response.loans[0].returned_at == ""
            MockLoanService.assert_called_once()
            mock_loan_service.list_all_loans.assert_called_with(page=1, limit=10)

    def test_return_book(self, service, mock_db_scope):
        mock_db = MagicMock()
        mock_db_scope.return_value.__enter__.return_value = mock_db
        
        with patch('backend.api.service.LoanService') as MockLoanService:
            mock_loan_service = MockLoanService.return_value
            
            mock_loan = MagicMock()
            mock_loan.id = "loan1"
            mock_loan.copy_id = "copy1"
            mock_loan.member_id = "member1"
            mock_loan.borrowed_at = datetime(2023, 1, 1)
            mock_loan.returned_at = datetime(2023, 1, 2)
            mock_loan_service.return_book.return_value = mock_loan
            
            mock_copy = MagicMock()
            mock_copy.metadata_rec.title = "Test Book"
            mock_db.query.return_value.filter_by.return_value.first.return_value = mock_copy

            request = library_pb2.ReturnBookRequest(loan_id="loan1")
            response = service.ReturnBook(request, None)
            
            assert response.id == "loan1"
            assert response.returned_at != ""
            mock_loan_service.return_book.assert_called_with("loan1")

    def test_list_member_loans(self, service, mock_db_scope):
        mock_db = MagicMock()
        mock_db_scope.return_value.__enter__.return_value = mock_db
        
        with patch('backend.api.service.LoanService') as MockLoanService:
            mock_loan_service = MockLoanService.return_value
            
            mock_loan_service.list_member_loans.return_value = {
                'loans': [],
                'total_count': 0,
                'total_pages': 0
            }
            
            request = library_pb2.ListMemberLoansRequest(member_id="m1", page=1, limit=10)
            response = service.ListMemberLoans(request, None)
            
            assert len(response.loans) == 0
            mock_loan_service.list_member_loans.assert_called_with("m1", page=1, limit=10)
