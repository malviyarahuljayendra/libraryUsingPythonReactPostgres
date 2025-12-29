import os
from ..infrastructure.session import engine
from ..infrastructure.models import (
    Base, AuthorModel, GenreModel, BookMetadataModel, BookCopyModel, MemberModel, LoanModel, book_genre
)

def init_db():
    recreate = os.getenv("DB_RECREATE", "false").lower() == "true"
    
    # Simple check for interactive environment or env var
    if recreate:
        print("!!! DB_RECREATE is TRUE. Dropping all tables... !!!")
        Base.metadata.drop_all(bind=engine)
    elif os.isatty(0): # Check if stdin is a terminal
        try:
            choice = input("Do you want to RECREATE the database schema? (y/N): ").lower()
            if choice == 'y':
                print("Dropping all tables...")
                Base.metadata.drop_all(bind=engine)
        except EOFError:
            pass # Non-interactive or piped
            
    Base.metadata.create_all(bind=engine)
