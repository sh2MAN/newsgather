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


DBASE = os.environ.get('POSTGRES_DB')
USER = os.environ.get('POSTGRES_USER')
PASS = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('DB_HOST')
PORT = os.environ.get('DB_PORT')

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DBASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
