from typing import List
from typing import Optional

from sqlalchemy.ext.declarative import DeclarativeMeta

from .config import get_logger
from .models import UrlData


logger = get_logger()


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

    def update(self, url_data: DeclarativeMeta) -> Optional[DeclarativeMeta]:
        """
        Update an existing UrlData record.

        Args:
            url_data (DeclarativeMeta): The UrlData object to update.

        Returns:
            DeclarativeMeta: The updated UrlData object.
        """

        self.session.add(url_data)
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

        url_data = self.session.query(UrlData).all()

        data = []
        for u in url_data:
            data.append({
                'id': u.id,
                'url': u.url,
                'title': str(u.title),
                'status_code': str(u.status_code),
                'js_hash': str(u.js_hash),
                'content_length': str(u.content_length),
                'added_time': str(u.added_time),
            })

        return data
