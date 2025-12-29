import sys
import os
import grpc

# Add generated code to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend/generated'))

import library_pb2
import library_pb2_grpc

def run():
    grpc_host = os.getenv("GRPC_HOST", "localhost")
    grpc_port = os.getenv("GRPC_PORT", "50051")
    target = f"{grpc_host}:{grpc_port}"
    print(f"Connecting to server at {target}...")
    with grpc.insecure_channel(target) as channel:
        stub = library_pb2_grpc.LibraryServiceStub(channel)
        
        # 1. Create Book
        print("\n--- Create Book ---")
        try:
            book = stub.CreateBook(library_pb2.CreateBookRequest(
                title="The Great Gatsby",
                author="F. Scott Fitzgerald",
                isbn="1234567890"
            ))
            print(f"Created Book: {book.title} (ID: {book.id})")
        except grpc.RpcError as e:
            print(f"Error creating book: {e.details()}")

        # 2. List Books
        print("\n--- List Books ---")
        books_response = stub.ListBooks(library_pb2.ListBooksRequest())
        for b in books_response.books:
            print(f"- {b.title} ({b.isbn}) Available: {b.is_available}")

        # 3. Create Member
        print("\n--- Create Member ---")
        try:
            member = stub.CreateMember(library_pb2.CreateMemberRequest(
                name="John Doe",
                email="john@example.com"
            ))
            print(f"Created Member: {member.name} (ID: {member.id})")
        except grpc.RpcError as e:
            print(f"Error creating member: {e.details()}")
            # fetch existing member for loan test if create failed (e.g. already exists from prev run)
            # In a real test we might want to list members to find one, but let's assume valid ID if I grep it,
            # or handle it gracefully. For now, if it fails, we might fail the next step unless we fetch.
            # Let's just catch and continue, maybe we can list members to pick one.
        
        # Get a member ID (pick the first one)
        members_resp = stub.ListMembers(library_pb2.ListMembersRequest())
        if not members_resp.members:
            print("No members found!")
            return
        member_id = members_resp.members[0].id
        print(f"Using Member ID: {member_id}")

        # Get a book ID
        books_resp = stub.ListBooks(library_pb2.ListBooksRequest())
        if not books_resp.books:
            print("No books found!")
            return
        book_id = books_resp.books[0].id
        print(f"Using Book ID: {book_id}")

        # 4. Borrow Book
        print("\n--- Borrow Book ---")
        try:
            loan = stub.BorrowBook(library_pb2.BorrowBookRequest(
                member_id=member_id,
                book_id=book_id
            ))
            print(f"Loan Created: {loan.id} at {loan.borrowed_at}")
        except grpc.RpcError as e:
            print(f"Error borrowing book: {e.details()}")

        # 5. List Loans
        print("\n--- List Loans ---")
        loans_resp = stub.ListMemberLoans(library_pb2.ListMemberLoansRequest(member_id=member_id))
        for l in loans_resp.loans:
            print(f"Loan: {l.id} - Book {l.book_id} - Returned: {l.returned_at}")

        # 6. Return Book
        print("\n--- Return Book ---")
        if loans_resp.loans:
            loan_id = loans_resp.loans[0].id
            try:
                returned_loan = stub.ReturnBook(library_pb2.ReturnBookRequest(loan_id=loan_id))
                print(f"Returned Loan: {returned_loan.id} at {returned_loan.returned_at}")
            except grpc.RpcError as e:
                print(f"Error returning book: {e.details()}")

if __name__ == '__main__':
    run()
