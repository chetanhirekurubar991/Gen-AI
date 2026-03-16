from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/mydb")

# Retry connection until DB is ready
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        break
    except Exception:
        print(f"DB not ready, retrying {i+1}/10...")
        time.sleep(2)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()