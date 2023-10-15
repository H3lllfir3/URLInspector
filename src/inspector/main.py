import json
import os
from datetime import datetime

from inspector.config import get_logger
from inspector.discord_client import DiscordWebhook
from inspector.models import UrlData
from inspector.queries import UrlDataQueries
from inspector.urlinspector import URLInspector


messages = []
logger = get_logger()


def main():

    all_records_json = json.loads(UrlDataQueries.get_all())

    for record in all_records_json:
        process_record(record)

    send_discord_messages()


def process_record(record):
    """Process a single URL record."""
    data = {i: j for i, j in record.items() if j is not None}
    domain = URLInspector(data['url'])
    url_data = UrlData.get(data['url'])

    if url_data:
        check_status_code_change(data, domain, url_data)
        check_title_change(data, domain, url_data)
        check_body_word(data, domain)
        check_content_length_change(data, domain, url_data)
        check_js_hash_change(data, domain, url_data)

        # Save the updated url_data
        url_data.update()


def check_status_code_change(data, domain, url_data):
    """Check if the status code has changed and update messages."""
    if data.get('status_code'):
        status_code = domain.check_status_code()
        if status_code != url_data.status_code:
            messages.append(
                f"Status code changed for {data['url']} from {url_data.status_code} to {status_code}",
            )
            logger.warning(f"Status code changed for {data['url']}")
            url_data.status_code = status_code


def check_title_change(data, domain, url_data):
    """Check if the title has changed and update messages."""
    if data.get('title'):
        title = domain.check_title()
        if title != url_data.title:
            messages.append(
                f"Title changed for {data['url']} from {url_data.title} to {title}",
            )
            logger.warning(f"Title changed for {data['url']}")
            url_data.title = title


def check_body_word(data, domain):
    """Check if the specified word is found in the body of the URL."""
    if data.get('body') and domain.check_word_in_body(data['body']):
        messages.append(
            f"Word '{data['body']}' found in body on {data['url']}",
        )
        logger.warning(
            f"Word '{data['body']}' found in body for {data['url']}",
        )


def check_content_length_change(data, domain, url_data):
    """Check if the content length has changed and update messages."""
    if data.get('content_length'):
        content_length = domain.check_content_length()
        if content_length != url_data.content_length:
            messages.append(
                f"Content length changed for {data['url']} from {url_data.content_length} to {content_length}",
            )
            logger.warning(f"Content length changed for {data['url']}")
            url_data.content_length = content_length


def check_js_hash_change(data, domain, url_data):
    """Check if JS file hashes have changed and update messages."""
    if data.get('js_hash'):
        old_url_hash_dict = {
            pair.split('|')[0]: pair.split(
                '|',
            )[1] for pair in url_data.js_hash.split(',')
        }
        new_url_hash_dict = {
            pair.split('|')[0]: pair.split(
                '|',
            )[1] for pair in domain.check_js_files().split(',')
        }

        for url, old_hash in old_url_hash_dict.items():
            if url in new_url_hash_dict and old_hash != new_url_hash_dict[url]:
                messages.append(f'JS file for {url} changed.')
                logger.info(
                    f'URL: {url}, Hash: {old_hash} -> {new_url_hash_dict[url]}',
                )
                old_url_hash_dict[url] = new_url_hash_dict[url]

        added_items = set(new_url_hash_dict.keys()) - \
            set(old_url_hash_dict.keys())
        if added_items:
            logger.warning('Added items:')
            for key in added_items:
                messages.append(f'JS file for {key} added.')
                logger.warning(f'[bold green]{key} added![/bold green]')
                old_url_hash_dict[key] = new_url_hash_dict.get(key, '')

        removed_items = set(old_url_hash_dict.keys()) - \
            set(new_url_hash_dict.keys())
        if removed_items:
            logger.warning('[bold red]Removed items:[/bold red]')
            keys_to_remove = []
            for key in removed_items:
                msg = {
                    'content': ':x:   **JS file removed at**!',
                    'embeds': [
                        {
                            'title': str(key),
                            'color': 'null',
                            'timestamp': datetime.now().strftime('%Y%m%d-%H%M%S'),
                        },
                    ],
                    'username': 'UrlSentry :eye:',
                    'avatar_url': 'https://github.com/zi-gax/Hunt/assets/67065043/e844e723-79c9-4913-b101-7a59d8d3eabe',
                    'attachments': [],
                }
                messages.append(msg)
                logger.warning(f'URL: {key}, Hash: {old_url_hash_dict[key]}')
                keys_to_remove.append(key)

            for key in keys_to_remove:
                old_url_hash_dict.pop(key)

        # Update the 'js_hash' field in the url_data object with the new hash data
        url_data.js_hash = ','.join(
            [f'{k}|{v}' for k, v in old_url_hash_dict.items()],
        )


def send_discord_messages():
    """Send messages to the Discord webhook in batches."""
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    discord = DiscordWebhook(webhook_url)

    for msg in messages:
        discord.send_message(msg)


if __name__ == '__main__':

    main()
