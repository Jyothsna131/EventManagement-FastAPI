from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url="mysql+pymysql://root:root123@localhost:3306/event_management"

engine=create_engine(db_url)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()