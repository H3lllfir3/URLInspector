import logging
import json
import os
from collections import defaultdict

from cli.queries import UrlData
from cli.url_sentry import URL
from bot import DiscordWebhook

from crontab import CronTab
from rich import print
from dotenv import load_dotenv


ENV_DIR = os.path.join(os.path.expanduser("~"), '.url_sentry')
LOG_FILE = os.path.join(ENV_DIR, 'log.txt')

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

messages = []

ENV_DIR = os.path.join(os.path.expanduser("~"), '.url_sentry')
ENV_FILE = '.env'
ENV_PATH = os.path.join(ENV_DIR, ENV_FILE)  # Replace with the actual path to your .env file
load_dotenv(ENV_PATH)

def main():
    # Load all records from JSON format
    all_records_json = json.loads(UrlData.get_all())
    
    # Iterate over each record and process it
    for record in all_records_json:
        process_record(record)

    # Send messages to the Discord webhook
    send_discord_messages()


def process_record(record):
    """Process a single URL record."""
    data = {i: j for i, j in record.items() if j is not None}
    domain = URL(data['url'])
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
            messages.append(f"Status code changed for {data['url']} from {url_data.status_code} to {status_code}")
            logging.warning(f"Status code changed for {data['url']}")
            url_data.status_code = status_code


def check_title_change(data, domain, url_data):
    """Check if the title has changed and update messages."""
    if data.get('title'):
        title = domain.check_title()
        if title != url_data.title:
            messages.append(f"Title changed for {data['url']} from {url_data.title} to {title}")
            logging.warning(f"Title changed for {data['url']}")
            url_data.title = title


def check_body_word(data, domain):
    """Check if the specified word is found in the body of the URL."""
    if data.get('body') and domain.check_word_in_body(data['body']):
        messages.append(f"Word '{data['body']}' found in body on {data['url']}")
        logging.warning(f"Word '{data['body']}' found in body for {data['url']}")


def check_content_length_change(data, domain, url_data):
    """Check if the content length has changed and update messages."""
    if data.get('content_length'):
        content_length = domain.check_content_length()
        if content_length != url_data.content_length:
            messages.append(f"Content length changed for {data['url']} from {url_data.content_length} to {content_length}")
            logging.warning(f"Content length changed for {data['url']}")
            url_data.content_length = content_length


def check_js_hash_change(data, domain, url_data):
    """Check if JS file hashes have changed and update messages."""
    if data.get('js_hash'):
        old_url_hash_dict = {pair.split('|')[0]: pair.split('|')[1] for pair in url_data.js_hash.split(',')}
        new_url_hash_dict = {pair.split('|')[0]: pair.split('|')[1] for pair in domain.check_js_files().split(',')}

        for url, old_hash in old_url_hash_dict.items():
            if url in new_url_hash_dict and old_hash != new_url_hash_dict[url]:
                messages.append(f"JS file for {url} changed.")
                logging.info(f"URL: {url}, Hash: {old_hash} -> {new_url_hash_dict[url]}")
                old_url_hash_dict[url] = new_url_hash_dict[url]

        added_items = set(new_url_hash_dict.keys()) - set(old_url_hash_dict.keys())
        if added_items:
            logging.warning("Added items:")
            for key in added_items:
                messages.append(f"JS file for {key} added.")
                logging.warning(f"[bold green]{key} added![/bold green]")
                old_url_hash_dict[key] = new_url_hash_dict.get(key, "")

        removed_items = set(old_url_hash_dict.keys()) - set(new_url_hash_dict.keys())
        if removed_items:
            logging.warning("[bold red]Removed items:[/bold red]")
            keys_to_remove = []
            for key in removed_items:
                messages.append(f"JS file removed at {key}")
                logging.warning(f"URL: {key}, Hash: {old_url_hash_dict[key]}")
                keys_to_remove.append(key)

            for key in keys_to_remove:
                old_url_hash_dict.pop(key)

        # Update the 'js_hash' field in the url_data object with the new hash data
        url_data.js_hash = ",".join([f"{k}|{v}" for k, v in old_url_hash_dict.items()])


def send_discord_messages():
    """Send messages to the Discord webhook in batches."""
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    discord = DiscordWebhook(webhook_url)

    chunk_size = 20
    for idx in range(0, len(messages), chunk_size):
        chunk_messages = messages[idx:idx + chunk_size]
        combined_message = "\n".join(chunk_messages)
        discord.send_message(combined_message)


def add_cron_job(script_path):
    """Add a cron job to run the script periodically."""
    cron = CronTab(user=True)

    python_path = "/usr/bin/python3"  # Change this to the path of your Python executable
    job = cron.new(command=f'{python_path} {script_path}', comment='url-sentry')
    job.setall('0 * * * *')  # This runs the job at the start of every hour

    try:
        cron.write()
        logging.info("[bold green]Cron job added successfully![/bold green]")
    except Exception as e:
        print()
        logging.warning(f"[bold red]Error adding cron job:[/bold red] {str(e)}")


def schedule_cron_job():
    try:
        script_path = os.path.abspath(__file__)
        add_cron_job(script_path)
    except Exception as e:
        logging.warning(f"Error adding cron job: {str(e)}")


if __name__ == '__main__':
    schedule_cron_job()
    main()
