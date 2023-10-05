import logging

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


logger = logging.getLogger(__name__)


def create_db(db_url: str) -> None:
    """
    Create the database schema.

    Args:
      db_url: Database URL
    """
    engine = create_engine(db_url)

    if not engine.dialect.has_table(engine, 'url_data'):
        logger.info('Creating tables')
        Base.metadata.create_all(engine)
    else:
        logger.info('Tables already present')


def run_migrations(alembic_ini: str) -> None:
    """Run Alembic migrations."""

    alembic_cfg = Config(alembic_ini)
    command.upgrade(alembic_cfg, 'head')


def get_session(db_url: str) -> sessionmaker:
    """
    Create a SQLAlchemy session for the database.
    Args:
      db_url: Database URL
    Return:
      Sessionmaker instance
    """
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()
