from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os
load_dotenv()
database_url :str |None = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("database url envirement varible is not set up or empty")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
    
engine = create_engine(database_url,echo = True)

SessionLocal = sessionmaker(autoflush = False,bind=engine)




def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    

