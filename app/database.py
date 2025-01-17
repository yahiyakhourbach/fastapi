from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .Config import settings

SQLALCHEMY_ENGINE_URL = f"postgresql://{settings.database_username}:{settings.password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_ENGINE_URL)

sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
