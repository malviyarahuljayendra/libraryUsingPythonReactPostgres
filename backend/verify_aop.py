import grpc
import uuid
import sys
import os

# Add generated to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'generated'))

import library_pb2
import library_pb2_grpc

def run_verification():
    print("🚀 Verifying AOP Centralized Error Handling...")
    channel = grpc.insecure_channel('localhost:50051')
    stub = library_pb2_grpc.LibraryServiceStub(channel)

    # 1. Test EntityNotFoundError (Update non-existent book)
    print("\n1️⃣  Testing EntityNotFoundError (Non-existent Book)")
    try:
        stub.UpdateBook(library_pb2.UpdateBookRequest(id=str(uuid.uuid4()), title="Ghost Book"))
    except grpc.RpcError as e:
        print(f"✅ Caught Expected Error: {e.code()} - {e.details()}")
        if e.code() != grpc.StatusCode.NOT_FOUND:
            print("❌ WRONG STATUS CODE! Expected NOT_FOUND")
    
    # 2. Test ConflictError (Duplicate ISBN)
    print("\n2️⃣  Testing ConflictError (Duplicate ISBN)")
    isbn = str(uuid.uuid4())[:10]
    stub.CreateBook(library_pb2.CreateBookRequest(title="Original", author="Author", isbn=isbn))
    try:
        stub.CreateBook(library_pb2.CreateBookRequest(title="Duplicate", author="Author", isbn=isbn))
    except grpc.RpcError as e:
        print(f"✅ Caught Expected Error: {e.code()} - {e.details()}")
        if e.code() != grpc.StatusCode.ALREADY_EXISTS:
            print("❌ WRONG STATUS CODE! Expected ALREADY_EXISTS")

    # 3. Test ValidationError (Double Borrow)
    print("\n3️⃣  Testing ValidationError (Double Borrow)")
    # Create a book and a member
    book = stub.CreateBook(library_pb2.CreateBookRequest(title="AOP Test Book", author="Author", isbn=str(uuid.uuid4())[:10]))
    member = stub.CreateMember(library_pb2.CreateMemberRequest(name="AOP Tester", email=f"aop_{uuid.uuid4().hex[:4]}@test.com"))
    
    # First borrow
    stub.BorrowBook(library_pb2.BorrowBookRequest(book_id=book.id, member_id=member.id))
    print("Book borrowed once.")
    
    try:
        # Second borrow same book
        stub.BorrowBook(library_pb2.BorrowBookRequest(book_id=book.id, member_id=member.id))
    except grpc.RpcError as e:
        print(f"✅ Caught Expected Error: {e.code()} - {e.details()}")
        if e.code() != grpc.StatusCode.FAILED_PRECONDITION:
            print("❌ WRONG STATUS CODE! Expected FAILED_PRECONDITION")

    print("\n✨ AOP Verification Complete!")

if __name__ == '__main__':
    run_verification()
