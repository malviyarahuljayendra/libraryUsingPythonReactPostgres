import pytest
from unittest.mock import MagicMock
from backend.services.author_service import AuthorService
from backend.core.database import AuthorModel

@pytest.fixture
def mock_session():
    return MagicMock()

def test_list_authors_pagination_logic(mock_session):
    service = AuthorService(mock_session)
    
    # Mock Repository paginated_list return
    # Returning 5 items with a total count of 12
    # Logic: limit=5, total=12 -> pages = ceil(12/5) = 3
    
    fake_items = [AuthorModel(id=str(i), name=f"A{i}") for i in range(5)]
    mock_session.query.return_value.count.return_value = 12
    mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = fake_items
    
    result = service.list_authors(page=1, limit=5)
    
    assert len(result['authors']) == 5
    assert result['total_count'] == 12
    assert result['total_pages'] == 3

def test_list_authors_empty_pagination(mock_session):
    service = AuthorService(mock_session)
    
    mock_session.query.return_value.count.return_value = 0
    mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
    
    result = service.list_authors(page=1, limit=10)
    
    assert len(result['authors']) == 0
    assert result['total_count'] == 0
    assert result['total_pages'] == 0
