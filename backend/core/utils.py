from contextlib import contextmanager
from backend.core.database.infrastructure.session import get_db

def build_paginated_response(items, total_count: int, limit: int, key_name: str) -> dict:
    """
    Constructs a standardized paginated response dictionary.
    
    Args:
        items: List of entities/models.
        total_count: Total number of records available.
        limit: Number of items per page.
        key_name: The key to use for the items list (e.g., 'authors', 'books').
        
    Returns:
        dict: Standardized response with items, total_count, and total_pages.
    """
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0
    return {
        key_name: items,
        "total_count": total_count,
        "total_pages": total_pages
    }

@contextmanager
def db_scope():
    """
    Context manager for database sessions with Global Transaction Management.
    - Yields a session.
    - Commits automatically on success.
    - Rolls back automatically on exception.
    - Maps SQLAlchemy exceptions to Domain exceptions.
    """
    from sqlalchemy.exc import IntegrityError, OperationalError
    from backend.core.exceptions import ConflictError, DatabaseError
    
    # get_db is a generator
    gen = get_db()
    session = next(gen)
    try:
        yield session
        session.commit()
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig) if e.orig else str(e)
        
        if "members_email_key" in error_info:
            raise ConflictError("Member with this email already exists")
        elif "members_name_key" in error_info: # If we had a name unique constraint
            raise ConflictError("Member with this name already exists")
        elif "books_metadata_isbn_key" in error_info:
            raise ConflictError("Book with this ISBN already exists")
        elif "genres_name_key" in error_info:
            raise ConflictError("Genre with this name already exists")
            
        # logger.warning(f"IntegrityError: {e}")
        raise ConflictError(f"Resource already exists (Database Constraint Violation)")
    except OperationalError as e:
        session.rollback()
        raise DatabaseError("Database unavailable")
    except Exception as e:
        session.rollback()
        raise
    finally:
        try:
            next(gen)
        except StopIteration:
            pass
        except Exception:
            session.close()
