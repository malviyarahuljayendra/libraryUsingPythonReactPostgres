import pytest
from unittest.mock import MagicMock, patch
from backend.services.book_service import BookService
from backend.core.database import BookMetadataModel
from backend.core.exceptions import ValidationError, ConflictError

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def book_service(mock_session):
    # We need to mock the repositories inside the service if we want true unit isolation,
    # or rely on the fact that the service init creates them with the session.
    # Here we mock the session which the repositories use.
    # Ideally, we would inject repositories, but for now we test with mocked session queries.
    return BookService(mock_session)

def test_create_book_success(book_service, mock_session):
    # Mock Repository behavior via session
    # get_by_isbn calls session.query...
    mock_session.query.return_value.filter_by.return_value.first.return_value = None 
    
    book = book_service.create_book(title="Test", isbn="1234567890")
    
    assert book.title == "Test"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_book_invalid_isbn(book_service):
    with pytest.raises(ValidationError):
        book_service.create_book(title="Test", isbn="123") 

def test_create_book_conflict(book_service, mock_session):
    # Mock existing book
    existing_book = BookMetadataModel(isbn="1234567890")
    mock_session.query.return_value.filter_by.return_value.first.return_value = existing_book
    
    with pytest.raises(ConflictError):
        book_service.create_book(title="Test", isbn="1234567890")

def test_list_books(book_service):
    mock_items = [BookMetadataModel(title="B1"), BookMetadataModel(title="B2")]
    book_service.repo.paginated_list = MagicMock(return_value=(mock_items, 2))
    
    result = book_service.list_books(page=1, limit=10)
    
    assert len(result['books']) == 2
    assert result['total_count'] == 2

def test_update_book_success(book_service, mock_session):
    existing_book = BookMetadataModel(id="1", title="Old Title", isbn="1234567890")
    book_service.repo.get_by_id = MagicMock(return_value=existing_book)
    book_service.repo.get_by_isbn = MagicMock(return_value=None)
    
    updated = book_service.update_book("1", title="New Title")
    
    assert updated.title == "New Title"
    mock_session.commit.assert_called_once()

def test_add_copy_success(book_service, mock_session):
    existing_book = BookMetadataModel(id="1")
    book_service.repo.get_by_id = MagicMock(return_value=existing_book)
    
    copy = book_service.add_copy("1")
    
    assert copy.book_metadata_id == "1"
    mock_session.commit.assert_called_once()

def test_list_copies(book_service):
    mock_items = [MagicMock(), MagicMock()]
    book_service.repo.paginated_list_copies = MagicMock(return_value=(mock_items, 2))
    
    result = book_service.list_copies("book1", page=1, limit=10)
    
    assert len(result['copies']) == 2
    assert result['total_count'] == 2
