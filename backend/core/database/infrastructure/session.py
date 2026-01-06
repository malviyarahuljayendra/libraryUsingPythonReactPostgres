from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.config import Config

DATABASE_URL = Config.get_database_url()
pool_config = Config.get_postgres_pool_config()

engine_args = {}
if "sqlite" not in DATABASE_URL:
    engine_args = {
        "pool_size": pool_config["pool_size"],
        "max_overflow": pool_config["max_overflow"],
        "pool_timeout": pool_config["pool_timeout"],
        "pool_recycle": pool_config["pool_recycle"],
        "pool_pre_ping": True
    }

engine = create_engine(DATABASE_URL, **engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
