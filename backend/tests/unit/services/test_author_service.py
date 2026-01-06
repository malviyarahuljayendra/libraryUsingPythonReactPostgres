import pytest
from unittest.mock import MagicMock
from backend.services.author_service import AuthorService
from backend.core.database import AuthorModel
from backend.core.exceptions import ValidationError

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def author_service(mock_session):
    return AuthorService(mock_session)

def test_create_author_success(author_service, mock_session):
    # Setup
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    
    # Execute
    result = author_service.create_author(name="New Author", bio="Bio")
    
    # Verify
    assert result.name == "New Author"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

def test_create_author_duplicate(author_service, mock_session):
    existing = AuthorModel(name="Tolkien")
    mock_session.query.return_value.filter_by.return_value.first.return_value = existing

    with pytest.raises(ValidationError) as exc:
        author_service.create_author(name="Tolkien")
    assert "already exists" in str(exc.value)

def test_create_author_validation_error(author_service):
    with pytest.raises(ValidationError):
        author_service.create_author(name="")
