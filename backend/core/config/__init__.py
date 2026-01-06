import os
from pydantic_settings import BaseSettings

from pydantic import model_validator
from typing import Optional

class Settings(BaseSettings):
    DB_USER: str = "library_user"
    DB_PASSWORD: str = "library_password"
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DB_NAME: str = "library_db"
    
    DATABASE_URL: Optional[str] = None
    GRPC_PORT: str = "50051"
    MAX_WORKERS: int = 10
    
    # DB Pooling
    POSTGRES_POOL_SIZE: int = 5
    POSTGRES_MAX_OVERFLOW: int = 10
    POSTGRES_POOL_TIMEOUT: int = 30
    POSTGRES_POOL_RECYCLE: int = 1800
    
    @model_validator(mode='after')
    def compute_database_url(self) -> 'Settings':
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return self

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

class Config:
    @staticmethod
    def get_database_url():
        return settings.DATABASE_URL

    @staticmethod
    def get_grpc_port():
        return settings.GRPC_PORT

    @staticmethod
    def get_max_workers():
        return settings.MAX_WORKERS

    @staticmethod
    def get_postgres_pool_config():
        return {
            "pool_size": settings.POSTGRES_POOL_SIZE,
            "max_overflow": settings.POSTGRES_MAX_OVERFLOW,
            "pool_timeout": settings.POSTGRES_POOL_TIMEOUT,
            "pool_recycle": settings.POSTGRES_POOL_RECYCLE
        }
