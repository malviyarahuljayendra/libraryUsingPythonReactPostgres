import grpc
import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

from backend.generated import library_pb2, library_pb2_grpc

def test_list_loans():
    print("Connecting to gRPC server at localhost:50051...")
    channel = grpc.insecure_channel('localhost:50051')
    stub = library_pb2_grpc.LibraryServiceStub(channel)

    print("Calling ListAllLoans...")
    try:
        response = stub.ListAllLoans(library_pb2.ListAllLoansRequest(page=1, limit=10))
        print("Response received:")
        print(f"Total Count: {response.total_count}")
        print(f"Loans: {len(response.loans)}")
        for loan in response.loans:
            print(f"- Loan {loan.id}: {loan.book_title} (Member: {loan.member_name or loan.member_id}, Returned: {loan.returned_at})")
    except grpc.RpcError as e:
        print(f"RPC Error: {e.code()} - {e.details()}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    test_list_loans()
