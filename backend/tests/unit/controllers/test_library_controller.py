import pytest
from unittest.mock import MagicMock, patch
from backend.api.service import LibraryService
from backend.generated import library_pb2
from backend.core.database import AuthorModel, GenreModel, BookMetadataModel, MemberModel, LoanModel
from datetime import datetime

@pytest.fixture
def mock_context():
    return MagicMock()

@pytest.fixture
def controller():
    return LibraryService()

@patch('backend.api.service.db_scope')
@patch('backend.api.service.AuthorService')
def test_create_author(MockAuthorService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockAuthorService.return_value
    expected_author = AuthorModel(id="123", name="Test Auth", bio="Bio")
    mock_service_instance.create_author.return_value = expected_author
    
    request = library_pb2.CreateAuthorRequest(name="Test Auth", bio="Bio")
    response = controller.CreateAuthor(request, mock_context)
    
    assert response.name == "Test Auth"
    assert mock_db_scope.return_value.__exit__.called

@patch('backend.api.service.db_scope')
@patch('backend.api.service.AuthorService')
def test_list_authors(MockAuthorService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockAuthorService.return_value
    mock_service_instance.list_authors.return_value = {
        'authors': [AuthorModel(id="1", name="A1")],
        'total_count': 1,
        'total_pages': 1
    }
    
    request = library_pb2.ListAuthorsRequest(page=1, limit=10)
    response = controller.ListAuthors(request, mock_context)
    
    assert len(response.authors) == 1
    assert response.total_count == 1

@patch('backend.api.service.db_scope')
@patch('backend.api.service.GenreService')
def test_create_genre(MockGenreService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockGenreService.return_value
    mock_service_instance.create_genre.return_value = GenreModel(id="1", name="G1")
    
    request = library_pb2.CreateGenreRequest(name="G1")
    response = controller.CreateGenre(request, mock_context)
    
    assert response.name == "G1"

@patch('backend.api.service.db_scope')
@patch('backend.api.service.BookService')
def test_create_book(MockBookService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockBookService.return_value
    
    # Mock book with author and genres for _map_book
    mock_book = MagicMock()
    mock_book.id = "b1"
    mock_book.title = "T1"
    mock_book.author = None
    mock_book.genres = []
    mock_book.copies = []
    mock_book.isbn = "123"
    
    mock_service_instance.create_book.return_value = mock_book
    
    request = library_pb2.CreateBookRequest(title="T1", isbn="123")
    response = controller.CreateBook(request, mock_context)
    
    assert response.title == "T1"

@patch('backend.api.service.db_scope')
@patch('backend.api.service.MemberService')
def test_create_member(MockMemberService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockMemberService.return_value
    mock_service_instance.create_member.return_value = MemberModel(id="m1", name="N1", email="e1")
    
    request = library_pb2.CreateMemberRequest(name="N1", email="e1")
    response = controller.CreateMember(request, mock_context)
    
    assert response.name == "N1"

@patch('backend.api.service.db_scope')
@patch('backend.api.service.LoanService')
def test_borrow_book(MockLoanService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockLoanService.return_value
    
    now = datetime.utcnow()
    mock_loan = MagicMock()
    mock_loan.id = "l1"
    mock_loan.copy_id = "c1"
    mock_loan.member_id = "m1"
    mock_loan.borrowed_at = now
    
    mock_service_instance.borrow_book.return_value = mock_loan
    # Mock DB query for copy title
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    
    request = library_pb2.BorrowBookRequest(book_id="b1", member_id="m1")
    response = controller.BorrowBook(request, mock_context)
    
    assert response.id == "l1"
    assert response.borrowed_at == now.isoformat()

@patch('backend.api.service.db_scope')
@patch('backend.api.service.GenreService')
def test_list_genres(MockGenreService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockGenreService.return_value
    mock_service_instance.list_genres.return_value = {
        'genres': [GenreModel(id="1", name="G1")],
        'total_count': 1,
        'total_pages': 1
    }
    
    request = library_pb2.ListGenresRequest(page=1, limit=10)
    response = controller.ListGenres(request, mock_context)
    
    assert len(response.genres) == 1
    assert response.total_count == 1

@patch('backend.api.service.db_scope')
@patch('backend.api.service.BookService')
def test_update_book(MockBookService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockBookService.return_value
    
    mock_book = MagicMock()
    mock_book.id = "b1"
    mock_book.title = "New T"
    mock_book.author = None
    mock_book.genres = []
    mock_book.copies = []
    mock_book.isbn = "123"
    
    mock_service_instance.update_book.return_value = mock_book
    
    request = library_pb2.UpdateBookRequest(id="b1", title="New T")
    response = controller.UpdateBook(request, mock_context)
    
    assert response.title == "New T"

@patch('backend.api.service.db_scope')
@patch('backend.api.service.BookService')
def test_add_book_copy(MockBookService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockBookService.return_value
    
    mock_copy = MagicMock()
    mock_copy.id = "c1"
    mock_copy.book_metadata_id = "b1"
    mock_copy.is_available = True
    mock_copy.status = "Available"
    
    mock_service_instance.add_copy.return_value = mock_copy
    
    request = library_pb2.AddBookCopyRequest(book_id="b1")
    response = controller.AddBookCopy(request, mock_context)
    
    assert response.id == "c1"

@patch('backend.api.service.db_scope')
@patch('backend.api.service.BookService')
def test_list_book_copies(MockBookService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockBookService.return_value
    
    mock_copy = MagicMock()
    mock_copy.id = "c1"
    mock_copy.book_metadata_id = "b1"
    mock_copy.is_available = True
    mock_copy.status = "Available"
    
    mock_service_instance.list_copies.return_value = {
        'copies': [mock_copy],
        'total_count': 1,
        'total_pages': 1
    }
    
    request = library_pb2.ListBookCopiesRequest(book_id="b1")
    response = controller.ListBookCopies(request, mock_context)
    
    assert len(response.copies) == 1

@patch('backend.api.service.db_scope')
@patch('backend.api.service.MemberService')
def test_list_members(MockMemberService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockMemberService.return_value
    mock_service_instance.list_members.return_value = {
        'members': [MemberModel(id="m1", name="N1", email="e1")],
        'total_count': 1,
        'total_pages': 1
    }
    
    request = library_pb2.ListMembersRequest(page=1, limit=10)
    response = controller.ListMembers(request, mock_context)
    
    assert len(response.members) == 1

@patch('backend.api.service.db_scope')
@patch('backend.api.service.MemberService')
def test_update_member(MockMemberService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockMemberService.return_value
    mock_service_instance.update_member.return_value = MemberModel(id="m1", name="New N", email="e1")
    
    request = library_pb2.UpdateMemberRequest(id="m1", name="New N")
    response = controller.UpdateMember(request, mock_context)
    
    assert response.name == "New N"

@patch('backend.api.service.db_scope')
@patch('backend.api.service.LoanService')
def test_return_book(MockLoanService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockLoanService.return_value
    
    now = datetime.utcnow()
    mock_loan = MagicMock()
    mock_loan.id = "l1"
    mock_loan.copy_id = "c1"
    mock_loan.member_id = "m1"
    mock_loan.borrowed_at = now
    mock_loan.returned_at = now
    
    mock_service_instance.return_book.return_value = mock_loan
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    
    request = library_pb2.ReturnBookRequest(loan_id="l1")
    response = controller.ReturnBook(request, mock_context)
    
    assert response.id == "l1"
    assert response.returned_at == now.isoformat()

@patch('backend.api.service.db_scope')
@patch('backend.api.service.LoanService')
def test_list_member_loans(MockLoanService, mock_db_scope, controller, mock_context):
    mock_db = MagicMock()
    mock_db_scope.return_value.__enter__.return_value = mock_db
    mock_service_instance = MockLoanService.return_value
    
    now = datetime.utcnow()
    mock_loan = MagicMock()
    mock_loan.id = "l1"
    mock_loan.copy_id = "c1"
    mock_loan.member_id = "m1"
    mock_loan.borrowed_at = now
    mock_loan.returned_at = None
    
    mock_service_instance.list_member_loans.return_value = {
        'loans': [mock_loan],
        'total_count': 1,
        'total_pages': 1
    }
    
    # Mock the relationships: l.copy.metadata_rec.title and l.member.name/.email
    mock_loan.copy.metadata_rec.title = "T1"
    mock_loan.member.name = "N1"
    mock_loan.member.email = "e1"
    
    request = library_pb2.ListMemberLoansRequest(member_id="m1")
    response = controller.ListMemberLoans(request, mock_context)
    
    assert len(response.loans) == 1
    assert response.loans[0].member_email == "e1"
