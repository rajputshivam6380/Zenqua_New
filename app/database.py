from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Create Engine
engine = create_engine(DATABASE_URL, echo=True)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base Class
Base = declarative_base()


# Dependency (used in FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()