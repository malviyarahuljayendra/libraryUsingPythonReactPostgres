import grpc
import sys
import os
import json

# Standardize project root for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.generated import library_pb2, library_pb2_grpc

def load_json(filename):
    data_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(data_path, 'r') as f:
        return json.load(f)

def seed():
    print("Seeding Database from JSON configuration...")
    
    grpc_host = os.getenv('GRPC_HOST', 'localhost')
    grpc_port = os.getenv('GRPC_PORT', '50051')
    target = f"{grpc_host}:{grpc_port}"
    
    print(f"Connecting to Backend at {target}...")
    channel = grpc.insecure_channel(target)
    stub = library_pb2_grpc.LibraryServiceStub(channel)

    try:
        # 1. Genres
        print("Processing Genres...")
        genres_data = load_json('genres.json')
        genre_map = {}
        for name in genres_data:
            g = stub.CreateGenre(library_pb2.CreateGenreRequest(name=name))
            genre_map[name] = g.id
            print(f"  - Created/Found Genre: {name}")

        # 2. Authors
        print("Processing Authors...")
        authors_data = load_json('authors.json')
        author_map = {}
        for item in authors_data:
            name = item['name']
            bio = item.get('bio', '')
            a = stub.CreateAuthor(library_pb2.CreateAuthorRequest(name=name, bio=bio))
            author_map[name] = a.id
            print(f"  - Created/Found Author: {name}")

        # 3. Books & Copies
        print("Processing Books & Copies...")
        books_data = load_json('books.json')
        for item in books_data:
            title = item['title']
            author_name = item['author_name']
            genre_names = item['genres']
            isbn = item['isbn']
            copy_count = item.get('copies', 1)

            author_id = author_map.get(author_name)
            genre_ids = [genre_map[gn] for gn in genre_names if gn in genre_map]

            try:
                b = stub.CreateBook(library_pb2.CreateBookRequest(
                    title=title, 
                    author_id=author_id, 
                    genre_ids=genre_ids, 
                    isbn=isbn
                ))
                print(f"  - Created Book: {title}")
                for _ in range(copy_count):
                    stub.AddBookCopy(library_pb2.AddBookCopyRequest(book_id=b.id))
                print(f"    - Added {copy_count} physical copies")
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                    print(f"  - Skipping Book: {title} (Already exists)")
                else:
                    raise e

        # 4. Members
        print("Processing Members...")
        members_data = load_json('members.json')
        for item in members_data:
            name = item['name']
            email = item['email']
            try:
                stub.CreateMember(library_pb2.CreateMemberRequest(name=name, email=email))
                print(f"  - Created Member: {name}")
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                    print(f"  - Skipping Member: {name} (Already exists)")
                else:
                    raise e

        print("\nSeeding Complete! The application is ready with a clean, unique dataset.")

    except Exception as e:
        print(f"Error during seeding: {e}")

if __name__ == "__main__":
    seed()
