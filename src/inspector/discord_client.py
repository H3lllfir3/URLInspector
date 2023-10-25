import json
from datetime import datetime

import requests

from .config import get_logger

logger = get_logger()


class DiscordMessage:
    """Class to generate a Discord message payload."""

    def __init__(self, title: str, url: str) -> None:
        """Initialize a DiscordMessage.

        Args:
            title (str): The title for the message embed.
            url (str): The url for the message embed.
        """
        self.title = title
        self.url = url

    def to_dict(self) -> dict:
        """Convert the message to a dictionary payload.

        Returns:
            Dict: The dictionary payload
        """

        return {
            'content': f':x:   **{self.title}**!',
            'embeds': [
                {
                    'title': self.url,
                    'color': 'null',
                    'timestamp': datetime.now().strftime('%Y%m%d-%H%M%S'),
                },
            ],
            'username': 'UrlSentry :eye:',
            'avatar_url': 'https://github.com/zi-gax/Hunt/assets/67065043/e844e723-79c9-4913-b101-7a59d8d3eabe',
            'attachments': [],
        }


class DiscordWebhook:
    """Class to send messages to a Discord webhook."""

    def __init__(self, webhook_url: str) -> None:
        """Initialize the webhook.

        Args:
            webhook_url (str): The Discord webhook URL.
        """
        self.webhook_url = webhook_url
        self.headers = {
            'Content-Type': 'application/json',
        }

    def send_message(self, title: str, url: str) -> None:
        """Send a message to the webhook.

        Args:
            title (str): The title for the Discord message.
            url (str): The url for the Discord message.
        """
        message = DiscordMessage(title, url)
        payload = message.to_dict()

        response = requests.post(
            self.webhook_url,
            data=json.dumps(payload),
            headers=self.headers,
        )

        if response.status_code == 204:
            logger.info('Message sent successfully.')
        else:
            logger.error(f'Failed to send message. Status code: {response.status_code}')
