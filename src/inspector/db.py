from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import get_logger
from .models import Base


logger = get_logger()


def create_db(db_url: str) -> None:
    """
    Create the database schema.

    Args:
      db_url: Database URL
    """
    engine = create_engine(db_url)
    connection = engine.connect()

    if not engine.dialect.has_table(connection, 'url_data'):
        logger.info('Creating tables')
        Base.metadata.create_all(engine)
    else:
        logger.info('Tables already present')

    connection.close()


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
