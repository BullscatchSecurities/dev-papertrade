import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from urllib.parse import quote

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
DB_HOST = quote(os.getenv("DB_HOST"))
DB_NAME = quote(os.getenv("DB_NAME"))
DB_USER = quote(os.getenv("DB_USER"))
DB_PASSWORD = quote(os.getenv("DB_PASSWORD"))
DB_PORT = os.getenv("DB_PORT", 5432)  # Default to 5432 if not specified

# Construct the database URL
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
print(DATABASE_URL)
# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
# Test connection
try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
