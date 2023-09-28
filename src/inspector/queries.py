from sqlalchemy.orm import sessionmaker

from .models import engine
from .models import UrlData


class UrlDataQueries:
    """Class for querying UrlData database model."""

    def __init__(self) -> None:
        """Initialize session for queries."""
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create(self, url: str) -> UrlData:
        """
        Create new UrlData record.
        Args:
            url (str): URL for record

        Returns:
            UrlData: New UrlData object added to database
        """

        new_url = UrlData(url=url)
        self.session.add(new_url)
        self.session.commit()
        return new_url

    def read(self, url: str) -> UrlData | None:
        """
        Get UrlData record by URL.
        Args:
            url (str): URL of record

        Returns:
            UrlData: Query result or None if not found
        """

        return self.session.query(UrlData).filter_by(url=url).first()

    def update(self, url: str, **kwargs) -> UrlData | None:
        """
        Update existing UrlData record.
        Args:
            url (str): URL of record to update
            **kwargs: Attributes to update and values

        Returns:
            UrlData: Updated UrlData object
        """

        url_data = self.read(url)
        if url_data:
            for attr, value in kwargs.items():
                setattr(url_data, attr, value)
            self.session.commit()
            return url_data

    def delete(self, url: str) -> bool:
        """
        Delete UrlData record.
        Args:
            url (str): URL of record to delete

        Returns:
            bool: True if deleted, False if not found
        """

        url_data = self.read(url)
        if url_data:
            self.session.delete(url_data)
            self.session.commit()
            return True
        else:
            return False

    def get_all(self) -> list[UrlData]:
        """
        Get all UrlData records.
        Returns:
            list: List of all UrlData objects
        """

        return self.session.query(UrlData).all()
