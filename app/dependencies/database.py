from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DB_HOST, DB_NAME, DB_PASS, DB_USER


def get_db_url() -> str:
    return f"postgresql+psycopg2::{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


engine = create_engine(get_db_url())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
