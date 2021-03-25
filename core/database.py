from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config(env_file="./.env")

USER = config('POSTGRES_USER')
PASS = config('POSTGRES_PASSWORD')
HOST = config('DB_HOST')
PORT = config('DB_PORT')
DBASE = config('POSTGRES_DB')

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DBASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
