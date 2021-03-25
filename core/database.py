import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = BASE_DIR / '.env'

if dotenv_file.exists():
    load_dotenv(dotenv_file)

USER = os.environ.get('PG_USER')
PASS = os.environ.get('PG_PASS')
HOST = os.environ.get('PG_HOST')
DATABASE = os.environ.get('PG_DB')

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASS}@{HOST}/{DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
