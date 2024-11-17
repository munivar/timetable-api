from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("## connecting to the database...")


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minute: int

    class Config:
        env_file = ".env"


settings = Settings()

# DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


try:
    # Create SQLAlchemy engine
    engine = create_engine(
        DATABASE_URL, echo=False
    )  # Set echo=True for SQL query logging

    # Create a configured "Session" class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Base class for declarative class definitions
    Base = declarative_base()

    logger.info("## database connected successfully")
except SQLAlchemyError as e:
    logger.error(f"## error connecting to the database: {e}")
    raise


def get_db():
    # database session generator.
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"## database session error: {e}")
        raise
    finally:
        db.close()
        logger.info("## database session closed")


# database dependency injection
database = Annotated[Session, Depends(get_db)]
