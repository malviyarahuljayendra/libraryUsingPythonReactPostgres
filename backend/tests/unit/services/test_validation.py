import pytest
from unittest.mock import MagicMock
from backend.services.author_service import AuthorService
from backend.services.book_service import BookService
from backend.services.member_service import MemberService
from backend.services.genre_service import GenreService
from backend.core.exceptions import ValidationError

@pytest.fixture
def mock_session():
    return MagicMock()

def test_author_validation(mock_session):
    service = AuthorService(mock_session)
    # Test Name Too Long
    with pytest.raises(ValidationError, match="must not exceed 100 characters"):
        service.create_author(name="A" * 101)

def test_genre_validation(mock_session):
    service = GenreService(mock_session)
    # Test Name Too Long
    with pytest.raises(ValidationError, match="must not exceed 50 characters"):
        service.create_genre(name="G" * 51)

def test_member_validation(mock_session):
    service = MemberService(mock_session)
    # Test Name Too Long
    with pytest.raises(ValidationError, match="must not exceed 100 characters"):
        service.create_member(name="M" * 101, email="valid@example.com")
    # Test Email Too Long
    with pytest.raises(ValidationError, match="must not exceed 255 characters"):
        long_email = "a" * 245 + "@example.com"
        service.create_member(name="Valid Name", email=long_email)

def test_book_validation(mock_session):
    service = BookService(mock_session)
    # Test Title Too Long
    with pytest.raises(ValidationError, match="must not exceed 200 characters"):
        service.create_book(title="T" * 201, isbn="1234567890")
    
    # Test Negative Copies
    with pytest.raises(ValidationError, match="cannot be negative"):
        service.create_book(title="Valid Title", isbn="1234567890", initial_copies=-1)
