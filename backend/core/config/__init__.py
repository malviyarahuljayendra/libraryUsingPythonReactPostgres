import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    GRPC_PORT = os.getenv("GRPC_PORT")
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "10"))

    @staticmethod
    def get_database_url():
        return Config.DATABASE_URL

    @staticmethod
    def get_grpc_port():
        return Config.GRPC_PORT

    @staticmethod
    def get_max_workers():
        return Config.MAX_WORKERS
