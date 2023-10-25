from inspector.config import DB_URL
from inspector.config import DISCORD_WEBHOOK_URL
from inspector.config import get_logger
from inspector.db import get_session
from inspector.discord_client import DiscordNotification
from inspector.queries import UrlDataQueries
from inspector.urlinspector import URLInspector

messages = []
logger = get_logger()
session = get_session(DB_URL)
queries = UrlDataQueries(session)


def main():

    all_records_json = queries.get_all()

    for record in all_records_json:

        process_record(record)

    send_discord_messages()


def process_record(record):
    """Process a single URL record."""

    data = {k: v for k, v in record.items() if v != 'None'}
    url = record['url']
    domain = URLInspector(data['url'])
    url_data = queries.get(url)

    if url_data:
        check_status_code_change(data, domain, url_data)
        check_title_change(data, domain, url_data)
        check_content_length_change(data, domain, url_data)
        check_js_hash_change(data, domain, url_data)

        # Save the updated url_data
        queries.update(url_data)


def check_status_code_change(data, domain, url_data):
    """Check if the status code has changed and update messages."""
    if not data.get('status_code'):
        return

    status_code = domain.check_status_code()

    if status_code == url_data.status_code:
        return

    messages.append(
        f"Status code changed from `{url_data.status_code}` to `{status_code}`|{data['url']}|blue",
    )
    logger.warning(f"Status code changed for {data['url']}")
    url_data.status_code = status_code


def check_title_change(data, domain, url_data):
    """Check if the title has changed and update messages."""
    if not data.get('title'):
        return

    title = domain.check_title()

    if title == url_data.title:
        return

    messages.append(f"Title changed from `{url_data.title}` to `{title}`|{data['url']}|blue")
    logger.warning(f"Title changed for {data['url']}")
    url_data.title = title


def check_content_length_change(data, domain, url_data):
    """Check if the content length has changed and update messages."""

    if not data.get('content_length'):
        return

    content_length = domain.check_content_length()

    if content_length == url_data.content_length:
        return

    messages.append(
        f"Content length changed from `{url_data.content_length}` to `{content_length}`|{data['url']}|blue",
    )
    logger.warning(f"Content length changed for {data['url']}")
    url_data.content_length = content_length


JS_FILE_CHANGED = 'JS file changed'
JS_FILE_ADDED = 'JS file added'
JS_FILE_REMOVED = 'JS file removed'


def check_js_hash_change(data, domain, url_data):

    if not data.get('js_hash'):
        return

    # Parse hashes
    current_hashes = _parse_hashes(url_data.js_hash)
    new_hashes = _parse_hashes(domain.check_js_files())

    # Handle added files
    changed_urls = _compare_hashes(current_hashes, new_hashes)

    for url in changed_urls:
        messages.append(f'{JS_FILE_CHANGED}|{url}|blue')

    added_files = _get_added_files(current_hashes, new_hashes)
    for url in added_files:
        messages.append(f'{JS_FILE_ADDED}|{url}|green')

    # Handle removed files
    removed_files = _get_removed_files(current_hashes, new_hashes)

    for url in removed_files:
        messages.append(f'{JS_FILE_REMOVED}|{url}|red')

    # Update url data
    url_data.js_hash = _create_hash_string(new_hashes)


def _parse_hashes(hash_string):
    hash_dict = {}
    for pair in hash_string.split(','):
        url, hash_url = pair.split('|')
        hash_dict[url] = hash_url
    return hash_dict


def _compare_hashes(current, new):
    changed_urls = []
    for url, current_hash in current.items():
        if url in new and current_hash != new[url]:
            changed_urls.append(url)
    return changed_urls


def _get_added_files(current, new):
    return list(set(new.keys()) - set(current.keys()))


def _get_removed_files(current, new):
    return list(set(current.keys()) - set(new.keys()))


def _create_hash_string(hash_dict):
    return ','.join([f'{key}|{value}' for key, value in hash_dict.items()])


def send_discord_messages():
    """Send messages to Discord."""
    webhook_url = DISCORD_WEBHOOK_URL
    discord = DiscordNotification(webhook_url)

    for message in messages:
        title, url, status = message.split('|')
        discord.send_message(title, url, status)


if __name__ == '__main__':

    main()
