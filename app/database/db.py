from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_app_db():
    db=LocalSession()
    try:
        yield db
    finally:
        db.close()