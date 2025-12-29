class LibraryError(Exception):
    """Base class for all library domain exceptions."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class EntityNotFoundError(LibraryError):
    """Raised when a requested entity (Book, Member, etc.) is not found."""
    pass

class ValidationError(LibraryError):
    """Raised when business validation rules are violated (e.g. book unavailable)."""
    pass

class ConflictError(LibraryError):
    """Raised when a unique constraint is violated (e.g. duplicate ISBN)."""
    pass
