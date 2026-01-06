import sys
import os

sys.path.append(os.getcwd())

from backend.core.utils import db_scope
from backend.core.database import LoanRepository

def run():
    print("Testing LoanRepository...")
    try:
        with db_scope() as db:
            repo = LoanRepository(db)
            print("Listing all loans...")
            items, total = repo.paginated_list_by_member(None, 1, 10)
            print(f"Found {total} loans.")
            for loan in items:
                print(f"ID: {loan.id}")
                print(f"  Member: {loan.member.name if loan.member else 'None'} ({loan.member_id})")
                print(f"  Borrowed: {loan.borrowed_at}")
                print(f"  Copy: {loan.copy.id if loan.copy else 'None'}")
                if loan.copy and loan.copy.metadata_rec:
                    print(f"  Book: {loan.copy.metadata_rec.title}")
    except Exception as e:
        print(f"FAILED with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run()
