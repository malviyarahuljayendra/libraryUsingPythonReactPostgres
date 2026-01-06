class ErrorMessages:
    # Author
    AUTHOR_NAME_REQUIRED = "Author name is required"
    AUTHOR_NAME_TOO_LONG = "Author name must not exceed {max} characters"
    
    # Genre
    GENRE_NAME_REQUIRED = "Genre name is required"
    GENRE_NAME_TOO_LONG = "Genre name must not exceed {max} characters"
    
    # Member
    MEMBER_NAME_REQUIRED = "Member name is required"
    MEMBER_NAME_TOO_LONG = "Member name must not exceed {max} characters"
    MEMBER_EMAIL_INVALID = "Invalid email format"
    MEMBER_EMAIL_TOO_LONG = "Email must not exceed {max} characters"
    MEMBER_EMAIL_EXISTS = "Member with this email already exists"
    MEMBER_NOT_FOUND = "Member not found"
    
    # Book
    BOOK_TITLE_REQUIRED = "Book title is required"
    BOOK_TITLE_TOO_LONG = "Book title must not exceed {max} characters"
    BOOK_COPIES_NEGATIVE = "Initial copies cannot be negative"
    BOOK_ISBN_REQUIRED = "ISBN is required"
    BOOK_ISBN_INVALID = "Invalid ISBN length (must be 10 or 13 digits)"
    BOOK_ISBN_EXISTS = "Book with this ISBN already exists"
    BOOK_NOT_FOUND = "Book not found"
    
    # General
    DB_ERROR = "Database operation failed"
