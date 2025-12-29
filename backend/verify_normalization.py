import grpc
import sys
import os
import uuid

# Add the project root to sys.path so we can import backend.generated
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.generated import library_pb2, library_pb2_grpc

def run_normalization_test():
    print("🧪 Verifying Advanced Normalization (Authors, Genres, Copies)...")
    # Increase retry logic just in case backend is still starting
    channel = grpc.insecure_channel('localhost:50051')
    stub = library_pb2_grpc.LibraryServiceStub(channel)

    # 1. Create Author
    print("\n1️⃣  Creating Author")
    author = stub.CreateAuthor(library_pb2.CreateAuthorRequest(name="J.K. Rowling", bio="Author of Harry Potter"))
    print(f"Created Author: {author.name} (ID: {author.id})")

    # 2. Create Genre
    print("\n2️⃣  Creating Genre")
    genre = stub.CreateGenre(library_pb2.CreateGenreRequest(name="Fantasy"))
    print(f"Created Genre: {genre.name} (ID: {genre.id})")

    # 3. Create Book Metadata
    print("\n3️⃣  Creating Book Metadata")
    isbn = f"HP-{str(uuid.uuid4())[:8]}"
    book = stub.CreateBook(library_pb2.CreateBookRequest(
        title="Harry Potter and the Sorcerer's Stone",
        isbn=isbn,
        author_id=author.id,
        genre_ids=[genre.id]
    ))
    print(f"Created Book: {book.title} by {book.author.name}")
    print(f"Genres: {[g.name for g in book.genres]}")

    # 4. Add Copies
    print("\n4️⃣  Adding Book Copies")
    stub.AddBookCopy(library_pb2.AddBookCopyRequest(book_id=book.id))
    stub.AddBookCopy(library_pb2.AddBookCopyRequest(book_id=book.id))
    print("Added 2 copies.")

    # 5. List and Verify
    print("\n5️⃣  Verifying Book List and Counts")
    books_response = stub.ListBooks(library_pb2.ListBooksRequest())
    found_book = next(b for b in books_response.books if b.id == book.id)
    print(f"Book: {found_book.title}, Total Copies: {found_book.total_copies}, Available: {found_book.available_copies}")
    
    if found_book.total_copies != 2 or found_book.available_copies != 2:
        print("❌ ERROR: Copy counts mismatch!")

    # 6. Borrow and Verify
    print("\n6️⃣  Testing Borrow Logic")
    member = stub.CreateMember(library_pb2.CreateMemberRequest(name="Ron Weasley", email="ron@hogwarts.com"))
    loan = stub.BorrowBook(library_pb2.BorrowBookRequest(book_id=book.id, member_id=member.id))
    print(f"Borrowed Copy: {loan.copy_id} for {loan.book_title}")

    books_response = stub.ListBooks(library_pb2.ListBooksRequest())
    found_book = next(b for b in books_response.books if b.id == book.id)
    print(f"Post-Borrow: Total {found_book.total_copies}, Available {found_book.available_copies}")

    if found_book.available_copies != 1:
        print("❌ ERROR: Availability not updated correctly!")

    print("\n✅ Normalization Verification Successful!")

if __name__ == '__main__':
    run_normalization_test()
