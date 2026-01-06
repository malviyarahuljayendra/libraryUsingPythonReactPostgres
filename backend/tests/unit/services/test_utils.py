import pytest
from backend.core.utils import build_paginated_response, db_scope
from unittest.mock import MagicMock, patch

def test_build_paginated_response():
    items = [1, 2, 3]
    result = build_paginated_response(items, 10, 3, "data")
    
    assert result["data"] == items
    assert result["total_count"] == 10
    assert result["total_pages"] == 4

def test_build_paginated_response_zero_limit():
    result = build_paginated_response([], 10, 0, "data")
    assert result["total_pages"] == 0

def test_db_scope_success():
    mock_session = MagicMock()
    mock_gen = iter([mock_session])
    
    with patch('backend.core.utils.get_db', return_value=mock_gen):
        with db_scope() as session:
            assert session == mock_session

def test_db_scope_exception():
    mock_session = MagicMock()
    # Generator that raises Exception when next() is called the second time
    def mock_gen_func():
        yield mock_session
        raise Exception("Force fallback")

    with patch('backend.core.utils.get_db', return_value=mock_gen_func()):
        try:
            with db_scope() as session:
                raise ValueError("Context Error")
        except ValueError:
            pass
    
    # In utils.py, the Exception("Force fallback") will be caught by "except Exception:", 
    # and session.close() will be called.
    mock_session.close.assert_called()
