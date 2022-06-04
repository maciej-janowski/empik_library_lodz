from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path


# Path to project directory
BASE_DIR = Path(__file__).resolve().parent.parent


SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR}\empik.db?check_same_thread=False"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()