import logging
import json
from collections import defaultdict

from cli.queries import UrlData
from cli.url_sentry import URL
from bot import DiscordWebhook

from rich import print
from decouple import config


# Set up logging configuration
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a defaultdict to store messages for each URL
messages = []
webhook_url = config('DISCORD_WEBHOOK_URL')

def main():
    # Load all records from JSON format
    all_records_json = json.loads(UrlData.get_all())
    
    # Iterate over each record
    for record in all_records_json:
        # Convert the record to a dictionary with non-None values
        data = {i: j for i, j in record.items() if j is not None}
        domain = URL(data['url'])  # Create a URL object from the 'url' field
        url_data = UrlData.get(data['url'])  # Get existing data for the URL if it exists
        
        if url_data:
            # Check if the 'status_code' field is present in the record
            if data.get('status_code'):
                # Get the current status code from the URL and check if it's different from the stored one
                status_code = domain.check_status_code()
                if status_code != url_data.status_code:
                    # If the status code changed, update the messages dictionary and log the warning
                    messages.append(f"Status code changed for {data['url']} from {url_data.status_code} to {status_code}")
                    logging.warning(f"Status code changed for {data['url']}")
                    url_data.status_code = status_code

            # Check if the 'title' field is present in the record
            if data.get('title'):
                # Get the current title from the URL and check if it's different from the stored one
                title = domain.check_title()
                if title != url_data.title:
                    # If the title changed, update the messages dictionary and log the warning
                    messages.append(f"Title changed for {data['url']} from {url_data.title} to {title}")
                    logging.warning(f"Title changed for {data['url']}")
                    url_data.title = title

            # Check if the 'body' field is present in the record
            if data.get('body'):
                # Check if the specified word is found in the body of the URL
                if domain.check_word_in_body(data['body']):
                    # If the word is found, update the messages dictionary and log the warning
                    messages.append(f"Word '{data['body']}' found in body on {data['url']}")
                    logging.warning(f"Word '{data['body']}' found in body for {data['url']}")
                    url_data.body = data['body']

            # Check if the 'content_length' field is present in the record
            if data.get('content_length'):
                # Get the current content length from the URL and check if it's different from the stored one
                content_length = domain.check_content_length()
                if content_length != url_data.content_length:
                    # If the content length changed, update the messages dictionary and log the warning
                    messages.append(f"Content length changed for {data['url']} from {url_data.content_length} to {content_length}")
                    logging.warning(f"Content length changed for {data['url']}")
                    url_data.content_length = content_length

            # Check if the 'js_hash' field is present in the record
            if data.get('js_hash'):
                # Split the existing hash data into a dictionary for easy comparison
                old_url_hash = url_data.js_hash.split(',')
                old_url_hash_dict = {pair.split('|')[0]: pair.split('|')[1] for pair in old_url_hash}
                # Get the new hash data from the URL and split it into a dictionary for comparison
                new_url_hash = domain.check_js_files().split(',')
                new_url_hash_dict = {pair.split('|')[0]: pair.split('|')[1] for pair in new_url_hash}

                # Compare each URL's hash from the old and new hash dictionaries
                for url, old_hash in old_url_hash_dict.items():
                    if url in new_url_hash_dict:
                        new_hash = new_url_hash_dict[url]
                        if old_hash != new_hash:
                            # If the hash has changed, update the messages dictionary and log the warning
                            messages.append(f"JS file for {url} changed.")
                            logging.info(f"URL: {url}, Hash: {old_hash} -> {new_hash}")
                            old_url_hash_dict[url] = new_hash

                # Find items that are present in the new hash dictionary but not in the old one
                added_items = set(new_url_hash_dict.keys()) - set(old_url_hash_dict.keys())
                if added_items:
                    # If there are added items, update the messages dictionary and log the warning
                    logging.warning("Added items:")
                    for key in added_items:
                        messages.append(f"JS file for {key} added.")
                        logging.warning(f"[bold green]{key} added![/bold green]")
                        # Update the old hash dictionary with the added items
                        old_url_hash_dict[key] = new_url_hash_dict.get(key, "")

                # Find items that are present in the old hash dictionary but not in the new one
                removed_items = set(old_url_hash_dict.keys()) - set(new_url_hash_dict.keys())
                if removed_items:
                    # If there are removed items, update the messages dictionary and log the warning
                    logging.warning("[bold red]Removed items:[/bold red]")
                    keys_to_remove = []
                    for key in removed_items:
                        messages.append(f"JS file removed at {key}")
                        logging.warning(f"URL: {key}, Hash: {old_url_hash_dict[key]}")
                        keys_to_remove.append(key)

                    # Remove the keys of removed items from the old hash dictionary
                    for key in keys_to_remove:
                        old_url_hash_dict.pop(key)

                # Update the 'js_hash' field in the url_data object with the new hash data
                url_data.js_hash = ",".join([f"{k}|{v}" for k, v in old_url_hash_dict.items()])

            # Save the updated url_data
            url_data.update()

    discord = DiscordWebhook(webhook_url)

    chunk_size = 20
    # Sending messages in batches to avoid Discord webhook rate limit.
    for idx in range(0, len(messages), chunk_size):
        chunk_messages = messages[idx:idx + chunk_size]
        combined_message = "\n".join(chunk_messages)
        discord.send_message(combined_message)


if __name__ == '__main__':
    main()

