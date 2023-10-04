import logging
from typing import List
from typing import Optional

from sqlalchemy.ext.declarative import DeclarativeMeta

from .models import UrlData


logger = logging.getLogger(__name__)


class UrlDataQueries:
    """Class for querying UrlData database model."""

    def __init__(self, session) -> None:
        """Initialize session for queries."""

        self.session = session

    def add(self, url_data: UrlData) -> UrlData:
        """
        Create a new UrlData record.

        Args:
            url_data (UrlData): The UrlData object to be added to the database.

        Returns:
            UrlData: The newly added UrlData object.
        """

        self.session.add(url_data)
        self.session.commit()
        logger.info(f'Added new UrlData {url_data.id}')
        return url_data

    def get(self, url: str) -> Optional[DeclarativeMeta]:
        """
        Retrieve a UrlData record by URL.

        Args:
            url (str): The URL of the record to retrieve.

        Returns:
            UrlData: The retrieved UrlData object, or None if not found.
        """

        return self.session.query(UrlData).filter(UrlData.url == url).first()

    def update(self, url: str, **kwargs) -> Optional[DeclarativeMeta]:
        """
        Update an existing UrlData record.

        Args:
            url (str): The URL of the record to update.
            **kwargs: Keyword arguments representing attributes to update and their new values.

        Returns:
            UrlData: The updated UrlData object, or None if the record is not found.
        """

        url_data = self.get(url)
        if url_data:
            for attr, value in kwargs.items():
                setattr(url_data, attr, value)
            self.session.commit()
            logger.info(f'Updated UrlData {url_data.id}')
            return url_data

    def delete(self, url: str) -> bool:
        """
        Delete a UrlData record.
        Args:
            url (str): The URL of the record to delete.

        Returns:
            bool: True if the record was deleted, False if it was not found.
        """

        url_data = self.get(url)
        if url_data:
            self.session.delete(url_data)
            self.session.commit()
            logger.info(f'Deleted UrlData {url_data.id}')
            return True
        return False

    def get_all(self) -> List[DeclarativeMeta]:
        """
        Retrive all UrlData records from the database.
        Returns:
            list[UrlData]: A list of all UrlData objects in the database.
        """

        return self.session.query(UrlData).all()
