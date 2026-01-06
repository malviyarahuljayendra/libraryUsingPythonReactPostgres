import pytest
from backend.services.author_service import AuthorService
from backend.core.database import AuthorModel

def test_pagination_end_to_end(db_session):
    # 1. Seed Data
    # Create 15 authors
    for i in range(15):
        db_session.add(AuthorModel(name=f"Author {i}", bio="Test Bio"))
    db_session.commit()
    
    service = AuthorService(db_session)
    
    # 2. Test Page 1 (Limit 10)
    # expected: 10 items, total 15, pages 2
    res1 = service.list_authors(page=1, limit=10)
    assert len(res1['authors']) == 10
    assert res1['total_count'] == 15
    assert res1['total_pages'] == 2
    assert res1['authors'][0].name == "Author 0"
    
    # 3. Test Page 2 (Limit 10)
    # expected: 5 items (indexes 10-14)
    res2 = service.list_authors(page=2, limit=10)
    assert len(res2['authors']) == 5
    assert res2['authors'][0].name == "Author 10"

def test_pagination_empty(db_session):
    service = AuthorService(db_session)
    res = service.list_authors(page=1, limit=10)
    assert len(res['authors']) == 0
    assert res['total_count'] == 0
