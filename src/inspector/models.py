import os

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


DB_DIR = os.path.join(os.path.expanduser('~'), '.inspector')
DB_FILE = 'data.db'
DB_PATH = os.path.join(DB_DIR, DB_FILE)

engine = create_engine(f'sqlite:///{DB_PATH}')
Base = declarative_base()


class UrlData(Base):

    __tablename__ = 'url_date'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)

    title = Column(String, default=None)
    status_code = Column(Integer, default=None)
    body = Column(String, default=None)
    js_hash = Column(String, default=None)
    content_length = Column(Integer, default=None)
    added_time = Column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    def __repr__(self):
        return f"<UrlData(url='{self.url}')>"


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
