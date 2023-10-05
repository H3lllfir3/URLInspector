from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class UrlData(Base):

    __tablename__ = 'url_data'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)

    title = Column(String, default=None)
    status_code = Column(Integer, default=None)
    js_hash = Column(String, default=None)
    content_length = Column(Integer, default=None)
    added_time = Column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    def __repr__(self):
        return f"<UrlData(url='{self.url}')>"
