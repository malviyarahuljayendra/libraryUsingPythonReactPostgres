import grpc
from concurrent import futures
from backend.generated import library_pb2, library_pb2_grpc
from backend.core.utils import db_scope
from backend.services import (
    BookService, MemberService, LoanService, AuthorService, GenreService
)
from backend.services.validators import (
    BookAvailabilityValidator, MemberExistenceValidator
)
from backend.core.database import BookCopyModel, MemberModel

class LibraryService(library_pb2_grpc.LibraryServiceServicer):
    
    # --- Authors ---
    def CreateAuthor(self, request, context):
        with db_scope() as db:
            service = AuthorService(db)
            author = service.create_author(request.name, request.bio)
            return library_pb2.Author(id=author.id, name=author.name, bio=author.bio or "")

    def ListAuthors(self, request, context):
        with db_scope() as db:
            service = AuthorService(db)
            result = service.list_authors(page=request.page or 1, limit=request.limit or 10)
            return library_pb2.ListAuthorsResponse(
                authors=[library_pb2.Author(id=a.id, name=a.name, bio=a.bio or "") for a in result['authors']],
                total_count=result['total_count'],
                total_pages=result['total_pages']
            )

    # --- Genres ---
    def CreateGenre(self, request, context):
        with db_scope() as db:
            service = GenreService(db)
            genre = service.create_genre(request.name)
            return library_pb2.Genre(id=genre.id, name=genre.name)

    def ListGenres(self, request, context):
        with db_scope() as db:
            service = GenreService(db)
            result = service.list_genres(page=request.page or 1, limit=request.limit or 10)
            return library_pb2.ListGenresResponse(
                genres=[library_pb2.Genre(id=g.id, name=g.name) for g in result['genres']],
                total_count=result['total_count'],
                total_pages=result['total_pages']
            )

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
        with db_scope() as db:
            service = BookService(db)
            book = service.create_book(
                request.title, 
                request.isbn, 
                request.author_id, 
                request.genre_ids,
                request.initial_copies
            )
            return self._map_book(book)

    def ListBooks(self, request, context):
        with db_scope() as db:
            service = BookService(db)
            result = service.list_books(page=request.page or 1, limit=request.limit or 10)
            return library_pb2.ListBooksResponse(
                books=[self._map_book(b) for b in result['books']],
                total_count=result['total_count'],
                total_pages=result['total_pages']
            )

    def UpdateBook(self, request, context):
        with db_scope() as db:
            service = BookService(db)
            author_id = request.author_id if request.HasField('author_id') else None
            title = request.title if request.HasField('title') else None
            isbn = request.isbn if request.HasField('isbn') else None
            
            book = service.update_book(request.id, title, isbn, author_id, request.genre_ids)
            return self._map_book(book)

    # --- Copies ---
    def AddBookCopy(self, request, context):
        with db_scope() as db:
            service = BookService(db)
            copy = service.add_copy(request.book_id)
            return library_pb2.BookCopy(
                id=copy.id,
                book_id=copy.book_metadata_id,
                is_available=copy.is_available,
                status=copy.status
            )

    def ListBookCopies(self, request, context):
        with db_scope() as db:
            service = BookService(db)
            result = service.list_copies(request.book_id, page=request.page or 1, limit=request.limit or 10)
            return library_pb2.ListBookCopiesResponse(
                copies=[
                    library_pb2.BookCopy(
                        id=c.id,
                        book_id=c.book_metadata_id,
                        is_available=c.is_available,
                        status=c.status
                    ) for c in result['copies']
                ],
                total_count=result['total_count'],
                total_pages=result['total_pages']
            )

    # --- Members ---
    def CreateMember(self, request, context):
        with db_scope() as db:
            service = MemberService(db)
            member = service.create_member(request.name, request.email)
            return library_pb2.Member(id=member.id, name=member.name, email=member.email)

    def ListMembers(self, request, context):
        with db_scope() as db:
            service = MemberService(db)
            result = service.list_members(page=request.page or 1, limit=request.limit or 10)
            return library_pb2.ListMembersResponse(
                members=[library_pb2.Member(id=m.id, name=m.name, email=m.email) for m in result['members']],
                total_count=result['total_count'],
                total_pages=result['total_pages']
            )

    def UpdateMember(self, request, context):
        with db_scope() as db:
            service = MemberService(db)
            name = request.name if request.HasField('name') else None
            email = request.email if request.HasField('email') else None
            
            member = service.update_member(request.id, name, email)
            return library_pb2.Member(id=member.id, name=member.name, email=member.email)

    # --- Loans ---
    def BorrowBook(self, request, context):
        with db_scope() as db:
            validators = [BookAvailabilityValidator(), MemberExistenceValidator()]
            service = LoanService(db, validators)
            copy_id = request.copy_id if request.HasField('copy_id') else None
            loan = service.borrow_book(request.book_id, request.member_id, copy_id)
            
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

    def ReturnBook(self, request, context):
        with db_scope() as db:
            service = LoanService(db, [])
            loan = service.return_book(request.loan_id)
            
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

    def ListMemberLoans(self, request, context):
        with db_scope() as db:
            service = LoanService(db, [])
            result = service.list_member_loans(request.member_id, page=request.page or 1, limit=request.limit or 10)
            
            response_loans = []
            for l in result['loans']:
                # Safe access using relationships
                title = l.copy.metadata_rec.title if (l.copy and l.copy.metadata_rec) else "Unknown"
                member_name = l.member.name if l.member else "Unknown"
                member_email = l.member.email if l.member else ""

                response_loans.append(
                    library_pb2.Loan(
                        id=l.id,
                        copy_id=l.copy_id,
                        book_title=title,
                        member_id=l.member_id,
                        member_name=member_name,
                        member_email=member_email,
                        borrowed_at=l.borrowed_at.isoformat(),
                        returned_at=l.returned_at.isoformat() if l.returned_at else ""
                    )
                )
            return library_pb2.ListLoansResponse(
                loans=response_loans,
                total_count=result['total_count'],
                total_pages=result['total_pages']
            )

    def ListAllLoans(self, request, context):
        with db_scope() as db:
            service = LoanService(db, [])
            result = service.list_all_loans(page=request.page or 1, limit=request.limit or 10)
            
            response_loans = []
            for l in result['loans']:
                # Safe access using relationships
                title = l.copy.metadata_rec.title if (l.copy and l.copy.metadata_rec) else "Unknown"
                member_name = l.member.name if l.member else "Unknown"
                member_email = l.member.email if l.member else ""

                response_loans.append(
                    library_pb2.Loan(
                        id=l.id,
                        copy_id=l.copy_id,
                        book_title=title,
                        member_id=l.member_id,
                        member_name=member_name,
                        member_email=member_email,
                        borrowed_at=l.borrowed_at.isoformat(),
                        returned_at=l.returned_at.isoformat() if l.returned_at else ""
                    )
                )
            return library_pb2.ListLoansResponse(
                loans=response_loans,
                total_count=result['total_count'],
                total_pages=result['total_pages']
            )
