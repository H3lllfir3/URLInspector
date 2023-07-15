import logging
import json
import typer
from rich import print
from queries import UrlData
from url_sentry import URL

logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    all_records_json = json.loads(UrlData.get_all())
    
    messages = {}
    for record in all_records_json:
        data = {i: j for i, j in record.items() if j is not None}
        domain = URL(data['url'])
        url_data = UrlData.get(data['url'])
        
        if url_data:
            if data.get('status_code'):
                status_code = domain.check_status_code()
                if status_code != url_data.status_code:
                    messages[data['url']] = f"Status code changed from {url_data.status_code} to {status_code}"
                    logging.warning(f"Status code changed for {data['url']}")
                    url_data.status_code = status_code

            if data.get('title'):
                title = domain.check_title()
                if title != url_data.title:
                    messages[data['url']] = f"Title changed from {url_data.title} to {title}"
                    logging.warning(f"Title changed for {data['url']}")
                    url_data.title = title

            if data.get('body'):
                if domain.check_word_in_body(data['body']):
                    messages[data['url']] = f"Word '{data['body']}' found in body"
                    logging.warning(f"Word '{data['body']}' found in body for {data['url']}")
                    url_data.body = data['body']

            if data.get('content_length'):
                content_length = domain.check_content_length()
                if content_length != url_data.content_length:
                    messages[data['url']] = f"Content length changed from {url_data.content_length} to {content_length}"
                    logging.warning(f"Content length changed for {data['url']}")
                    url_data.content_length = content_length

            if data.get('js_hash'):
                old_url_hash = url_data.js_hash.split(',')
                old_url_hash_dict = {pair.split('|')[0]: pair.split('|')[1] for pair in old_url_hash}
                new_url_hash = domain.check_js_files().split(',')
                new_url_hash_dict = {pair.split('|')[0]: pair.split('|')[1] for pair in new_url_hash}

                for url, old_hash in old_url_hash_dict.items():
                    if url in new_url_hash_dict:
                        new_hash = new_url_hash_dict[url]
                        if old_hash != new_hash:
                            messages[url] = f"JS file with hash {new_hash} changed."
                            logging.warning(f"URL: {url}, Hash: {old_hash} -> {new_hash}")
                            old_url_hash_dict[url] = new_hash

                added_items = set(new_url_hash_dict.keys()) - set(old_url_hash_dict.keys())
                if added_items:
                    logging.warning("Added items:")
                    for key in added_items:
                        messages[data['url']] = f"JS file {key} added."
                        logging.warning(f"[bold red]{key} added![/bold red]")
                        old_url_hash_dict[key] = new_url_hash_dict[key]

                removed_items = set(old_url_hash_dict.keys()) - set(new_url_hash_dict.keys())
                if removed_items:
                    logging.warning("[bold red]Removed items:[/bold red]")
                    for key in removed_items:
                        messages[data['url']] = f"JS file {key} removed."
                        logging.warning(f"URL: {key}, Hash: {old_url_hash_dict[key]}")
                        old_url_hash_dict.pop(key)

                url_data.js_hash = ",".join([f"{k}|{v}" for k, v in old_url_hash_dict.items()])

            url_data.update()

    for url, message in messages.items():
        print(f"{url}: {message}")


if __name__ == '__main__':
    typer.run(main)
