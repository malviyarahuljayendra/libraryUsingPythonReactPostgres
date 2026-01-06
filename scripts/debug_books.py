import grpc
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.generated import library_pb2, library_pb2_grpc

def run():
    print("Connecting to gRPC server at localhost:50051...")
    channel = grpc.insecure_channel('localhost:50051')
    stub = library_pb2_grpc.LibraryServiceStub(channel)

    print("Calling ListBooks...")
    try:
        response = stub.ListBooks(library_pb2.ListBooksRequest(page=1, limit=10))
        print("Response received:")
        print(f"Total Count: {response.total_count}")
        print(f"Books: {len(response.books)}")
        for book in response.books:
            print(f"- {book.title} (ISBN: {book.isbn})")
    except grpc.RpcError as e:
        print(f"RPC Error: {e.code()} - {e.details()}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == '__main__':
    run()
