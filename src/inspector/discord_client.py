import json

import requests

from .config import get_logger

logger = get_logger()


class DiscordWebhook:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.headers = {
            'Content-Type': 'application/json',
        }

    def send_message(self, content):
        payload = {
            'content': content,
        }

        response = requests.post(
            self.webhook_url, data=json.dumps(payload), headers=self.headers,
        )

        if response.status_code == 204:
            logger.info('Message sent successfully.')
        else:
            logger.error(f'Failed to send message. Status code: {response.status_code}')
