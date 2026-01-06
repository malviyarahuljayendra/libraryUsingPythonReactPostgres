import pytest
from unittest.mock import MagicMock
from backend.services.genre_service import GenreService
from backend.core.database import GenreModel
from backend.core.exceptions import ValidationError
from backend.core.messages import ErrorMessages
from backend.core.constants import Limits

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def genre_service(mock_session):
    return GenreService(mock_session)

def test_create_genre_success(genre_service, mock_session):
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    
    genre = genre_service.create_genre(name="Fiction")
    
    assert genre.name == "Fiction"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_genre_invalid_name(genre_service):
    with pytest.raises(ValidationError) as exc:
        genre_service.create_genre(name="")
    assert str(exc.value) == ErrorMessages.GENRE_NAME_REQUIRED

def test_create_genre_name_too_long(genre_service):
    long_name = "g" * (Limits.GENRE_NAME_MAX + 1)
    with pytest.raises(ValidationError) as exc:
        genre_service.create_genre(name=long_name)
    assert str(exc.value) == ErrorMessages.GENRE_NAME_TOO_LONG.format(max=Limits.GENRE_NAME_MAX)

def test_create_genre_existing(genre_service, mock_session):
    existing = GenreModel(name="Fiction")
    mock_session.query.return_value.filter_by.return_value.first.return_value = existing
    
    with pytest.raises(ValidationError) as exc:
        genre_service.create_genre(name="Fiction")
    assert "already exists" in str(exc.value)

def test_list_genres(genre_service):
    mock_items = [GenreModel(name="G1"), GenreModel(name="G2")]
    genre_service.repo.paginated_list = MagicMock(return_value=(mock_items, 2))
    
    result = genre_service.list_genres(page=1, limit=10)
    
    assert len(result['genres']) == 2
    assert result['total_count'] == 2
