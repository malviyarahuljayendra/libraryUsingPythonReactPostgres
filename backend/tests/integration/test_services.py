import pytest
import grpc
from unittest.mock import MagicMock
from backend.api.service import LibraryService
from backend.generated import library_pb2
from google.protobuf.json_format import MessageToDict

@pytest.fixture
def service():
    return LibraryService()

@pytest.fixture
def context(db_session):
    # Mocking the context to intercept metadata if needed, 
    # but more importantly we need to patch the session used by the service methods
    # Since mapped service uses Next(get_db()), we might need to override dependency injection
    # For this simple test, we can treat the service methods as isolated if we can inject session.
    # However, LibraryService instantiates Managers with 'db = next(get_db())' inside the methods.
    # We should patch 'get_db' in service.py to return our test fixture db.
    return MagicMock()

def test_full_flow_create_and_list_books(db_session, monkeypatch, context):
    from contextlib import contextmanager
    @contextmanager
    def mock_db_scope():
        yield db_session
    
    monkeypatch.setattr("backend.api.service.db_scope", mock_db_scope)
    
    service = LibraryService()
    
    # 1. Create Author
    author_req = library_pb2.CreateAuthorRequest(name="Integration Author", bio="Test Bio")
    author_res = service.CreateAuthor(author_req, context)
    assert author_res.name == "Integration Author"
    author_id = author_res.id

    # 2. Create Book
    book_req = library_pb2.CreateBookRequest(
        title="Integration Book",
        isbn="978-0-123-45678-9",
        author_id=author_id,
        initial_copies=3
    )
    book_res = service.CreateBook(book_req, context)
    assert book_res.title == "Integration Book"
    assert book_res.isbn == "978-0-123-45678-9"
    assert book_res.available_copies == 3

    # 3. List Books (Verify Pagination)
    list_req = library_pb2.ListBooksRequest(page=1, limit=10)
    list_res = service.ListBooks(list_req, context)
    
    assert list_res.total_count == 1
    assert len(list_res.books) == 1
    assert list_res.books[0].title == "Integration Book"

def test_exception_mapping(db_session, monkeypatch, context):
    from contextlib import contextmanager
    @contextmanager
    def mock_db_scope():
        yield db_session
    monkeypatch.setattr("backend.api.service.db_scope", mock_db_scope)
    
    service = LibraryService()
    
    # Try creating invalid book (missing title is checked in Manager, but empty string here)
    # The proto definitions might allow empty strings, so validation in manager will raise ValidationError.
    # The interceptor normally handles this, but since we are calling method directly, exception will raise.
    
    from backend.core.exceptions import ValidationError
    
    with pytest.raises(ValidationError):
        req = library_pb2.CreateBookRequest(title="", isbn="123")
        service.CreateBook(req, context)
