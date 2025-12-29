import sys
import os
import grpc
from concurrent import futures
import time

from backend.generated import library_pb2_grpc
from backend.api.service import LibraryService
from backend.core.database import init_db

from backend.core.config import Config
from backend.api.middleware import ExceptionInterceptor

def serve():
    print("Initializing Database...")
    init_db()
    
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=Config.get_max_workers()),
        interceptors=(ExceptionInterceptor(),)
    )
    library_pb2_grpc.add_LibraryServiceServicer_to_server(LibraryService(), server)
    
    port = f'[::]:{Config.get_grpc_port()}'
    server.add_insecure_port(port)
    print(f"Server started on {port}")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
