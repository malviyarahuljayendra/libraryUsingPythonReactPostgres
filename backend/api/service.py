import grpc
from concurrent import futures
from backend.generated import library_pb2, library_pb2_grpc
from backend.core.database.infrastructure.session import get_db
from backend.services.managers import (
    BookManager, MemberManager, LoanManager, AuthorManager, GenreManager
)
from backend.services.validators import (
    BookAvailabilityValidator, MemberExistenceValidator
)
from backend.core.database import BookCopyModel

class LibraryService(library_pb2_grpc.LibraryServiceServicer):
    
    # --- Authors ---
    def CreateAuthor(self, request, context):
        db = next(get_db())
        try:
            manager = AuthorManager(db)
            author = manager.create_author(request.name, request.bio)
            return library_pb2.Author(id=author.id, name=author.name, bio=author.bio or "")
        finally:
            db.close()

    def ListAuthors(self, request, context):
        db = next(get_db())
        try:
            manager = AuthorManager(db)
            authors = manager.list_authors()
            return library_pb2.ListAuthorsResponse(
                authors=[library_pb2.Author(id=a.id, name=a.name, bio=a.bio or "") for a in authors]
            )
        finally:
            db.close()

    # --- Genres ---
    def CreateGenre(self, request, context):
        db = next(get_db())
        try:
            manager = GenreManager(db)
            genre = manager.create_genre(request.name)
            return library_pb2.Genre(id=genre.id, name=genre.name)
        finally:
            db.close()

    def ListGenres(self, request, context):
        db = next(get_db())
        try:
            manager = GenreManager(db)
            genres = manager.list_genres()
            return library_pb2.ListGenresResponse(
                genres=[library_pb2.Genre(id=g.id, name=g.name) for g in genres]
            )
        finally:
            db.close()

    # --- Books ---
    def _map_book(self, book):
        return library_pb2.Book(
            id=book.id,
            title=book.title,
            author=library_pb2.Author(
                id=book.author.id, 
                name=book.author.name, 
                bio=book.author.bio or ""
            ) if book.author else None,
            isbn=book.isbn,
            genres=[library_pb2.Genre(id=g.id, name=g.name) for g in book.genres],
            total_copies=len(book.copies),
            available_copies=len([c for c in book.copies if c.is_available])
        )

    def CreateBook(self, request, context):
        db = next(get_db())
        try:
            manager = BookManager(db)
            book = manager.create_book(
                request.title, 
                request.isbn, 
                request.author_id, 
                request.genre_ids,
                request.initial_copies
            )
            return self._map_book(book)
        finally:
            db.close()

    def ListBooks(self, request, context):
        db = next(get_db())
        try:
            manager = BookManager(db)
            books = manager.list_books()
            return library_pb2.ListBooksResponse(books=[self._map_book(b) for b in books])
        finally:
            db.close()

    def UpdateBook(self, request, context):
        db = next(get_db())
        try:
            manager = BookManager(db)
            author_id = request.author_id if request.HasField('author_id') else None
            title = request.title if request.HasField('title') else None
            isbn = request.isbn if request.HasField('isbn') else None
            
            book = manager.update_book(request.id, title, isbn, author_id, request.genre_ids)
            return self._map_book(book)
        finally:
            db.close()

    # --- Copies ---
    def AddBookCopy(self, request, context):
        db = next(get_db())
        try:
            manager = BookManager(db)
            copy = manager.add_copy(request.book_id)
            return library_pb2.BookCopy(
                id=copy.id,
                book_id=copy.book_metadata_id,
                is_available=copy.is_available,
                status=copy.status
            )
        finally:
            db.close()

    def ListBookCopies(self, request, context):
        db = next(get_db())
        try:
            manager = BookManager(db)
            copies = manager.list_copies(request.book_id)
            return library_pb2.ListBookCopiesResponse(
                copies=[
                    library_pb2.BookCopy(
                        id=c.id,
                        book_id=c.book_metadata_id,
                        is_available=c.is_available,
                        status=c.status
                    ) for c in copies
                ]
            )
        finally:
            db.close()

    # --- Members ---
    def CreateMember(self, request, context):
        db = next(get_db())
        try:
            manager = MemberManager(db)
            member = manager.create_member(request.name, request.email)
            return library_pb2.Member(id=member.id, name=member.name, email=member.email)
        finally:
            db.close()

    def ListMembers(self, request, context):
        db = next(get_db())
        try:
            manager = MemberManager(db)
            members = manager.list_members()
            return library_pb2.ListMembersResponse(
                members=[library_pb2.Member(id=m.id, name=m.name, email=m.email) for m in members]
            )
        finally:
            db.close()

    def UpdateMember(self, request, context):
        db = next(get_db())
        try:
            manager = MemberManager(db)
            name = request.name if request.HasField('name') else None
            email = request.email if request.HasField('email') else None
            
            member = manager.update_member(request.id, name, email)
            return library_pb2.Member(id=member.id, name=member.name, email=member.email)
        finally:
            db.close()

    # --- Loans ---
    def BorrowBook(self, request, context):
        db = next(get_db())
        try:
            validators = [BookAvailabilityValidator(), MemberExistenceValidator()]
            manager = LoanManager(db, validators)
            copy_id = request.copy_id if request.HasField('copy_id') else None
            loan = manager.borrow_book(request.book_id, request.member_id, copy_id)
            
            # Find copy to get book title
            copy = db.query(BookCopyModel).filter_by(id=loan.copy_id).first()
            title = copy.metadata_rec.title if copy else "Unknown"

            return library_pb2.Loan(
                id=loan.id,
                copy_id=loan.copy_id,
                book_title=title,
                member_id=loan.member_id,
                borrowed_at=loan.borrowed_at.isoformat(),
                returned_at=""
            )
        finally:
            db.close()

    def ReturnBook(self, request, context):
        db = next(get_db())
        try:
            manager = LoanManager(db, [])
            loan = manager.return_book(request.loan_id)
            
            copy = db.query(BookCopyModel).filter_by(id=loan.copy_id).first()
            title = copy.metadata_rec.title if copy else "Unknown"

            return library_pb2.Loan(
                id=loan.id,
                copy_id=loan.copy_id,
                book_title=title,
                member_id=loan.member_id,
                borrowed_at=loan.borrowed_at.isoformat(),
                returned_at=loan.returned_at.isoformat()
            )
        finally:
            db.close()

    def ListMemberLoans(self, request, context):
        db = next(get_db())
        try:
            manager = LoanManager(db, [])
            loans = manager.list_member_loans(request.member_id)
            
            # This would benefit from a more efficient query or join
            response_loans = []
            for l in loans:
                copy = db.query(BookCopyModel).filter_by(id=l.copy_id).first()
                title = copy.metadata_rec.title if copy else "Unknown"
                response_loans.append(
                    library_pb2.Loan(
                        id=l.id,
                        copy_id=l.copy_id,
                        book_title=title,
                        member_id=l.member_id,
                        borrowed_at=l.borrowed_at.isoformat(),
                        returned_at=l.returned_at.isoformat() if l.returned_at else ""
                    )
                )
            return library_pb2.ListLoansResponse(loans=response_loans)
        finally:
            db.close()
