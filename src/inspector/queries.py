from sqlalchemy.orm import sessionmaker

from .models import engine
from .models import UrlData


class UrlDataQueries:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create(self, url):
        new_url = UrlData(url=url)
        self.session.add(new_url)
        self.session.commit()
        return new_url

    def read(self, url):
        return self.session.query(UrlData).filter_by(url=url).first()

    def update(self, url, **kwargs):
        url_data = self.read(url)
        if url_data:
            for attr, value in kwargs.items():
                setattr(url_data, attr, value)
            self.session.commit()
            return url_data

    def delete(self, url):
        url_data = self.read(url)
        if url_data:
            self.session.delete(url_data)
            self.session.commit()
            return True
        else:
            return False

    def get_all(self):
        return self.session.query(UrlData).all()
