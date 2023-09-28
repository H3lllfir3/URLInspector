#!/usr/bin/env python
from __future__ import annotations

import argparse
import logging
import os

from rich import print

from .models import UrlData
from .urlinspector import URLInspector


def main():
    """Manage URL Data monitoring using CLI."""
    # Configure the logging
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    # Create a logger for the CLI
    cli_logger = logging.getLogger('cli_logger')
    cli_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    cli_logger.addHandler(console_handler)

    parser = argparse.ArgumentParser(description='URL Data Management')
    parser.add_argument(
        'action', nargs='?', choices=[
            'add', 'remove',
        ], help='Action to perform: add or remove',
    )
    parser.add_argument('-u', '--url', help='URL of the data')
    parser.add_argument(
        '-l', '--list', help='Path to a file containing a list of URLs',
    )
    parser.add_argument(
        '-status-code', action='store_true',
        help='Include status code',
    )
    parser.add_argument('-title', action='store_true', help='Include title')
    parser.add_argument('-js', action='store_true', help='Include JS')
    parser.add_argument(
        '-subs', action='store_true',
        help='Include all records',
    )
    parser.add_argument(
        '-content-length', action='store_true',
        help='Include content length',
    )
    parser.add_argument(
        '-body', action='store_true',
        help='Content of the body',
    )
    parser.add_argument('-logs', action='store_true', help='Show logs')
    parser.add_argument('--set_hook', help='Webhook URL')

    args = parser.parse_args()

    if args.set_hook:
        webhook_url = args.set_hook.strip()

        ENV_DIR = os.path.join(os.path.expanduser('~'), '.inspector')
        ENV_FILE = '.env'
        ENV_PATH = os.path.join(ENV_DIR, ENV_FILE)

        with open(ENV_PATH, 'w') as env_file:
            env_file.write(f'DISCORD_WEBHOOK_URL={webhook_url}\n')
        print('Webhook URL set successfully!')

    elif args.action == 'add':
        if args.list:
            with open(args.list) as file:
                urls = file.readlines()
            urls = [url.strip() for url in urls]

            for url in urls:
                url_data = UrlData.get(url)
                if url_data:
                    if args.status_code:
                        url_data.status_code = URLInspector(
                            url,
                        ).check_status_code()
                    if args.title:
                        url_data.title = URLInspector(url).check_title()
                    if args.js:
                        url_data.js_hash = URLInspector(url).check_js_files()
                    if args.content_length:
                        url_data.content_length = URLInspector(
                            url,
                        ).check_content_length()
                    url_data.update()
                    print(f'Data for URL {url} updated successfully!')
                else:
                    url_data = UrlData(url=url)
                    domain = URLInspector(url)
                    if args.status_code:
                        url_data.status_code = domain.check_status_code()
                    if args.title:
                        url_data.title = domain.check_title()
                    if args.js:
                        url_data.js_hash = domain.check_js_files()
                    if args.content_length:
                        url_data.content_length = domain.check_content_length()
                    url_data.save()
                    print(f'Data for URL {url} added successfully!')

        elif args.url:
            url_data = UrlData.get(args.url)
            if url_data:
                if args.status_code:
                    url_data.status_code = URLInspector(
                        args.url,
                    ).check_status_code()
                if args.title:
                    url_data.title = URLInspector(args.url).check_title()
                if args.js:
                    url_data.js_hash = URLInspector(args.url).check_js_files()
                if args.content_length:
                    url_data.content_length = URLInspector(
                        args.url,
                    ).check_content_length()
                url_data.update()
                print(f'Data for URL {args.url} updated successfully!')
            else:
                url_data = UrlData(url=args.url)
                domain = URLInspector(args.url)
                if args.status_code:
                    url_data.status_code = domain.check_status_code()
                if args.title:
                    url_data.title = domain.check_title()
                if args.js:
                    url_data.js_hash = domain.check_js_files()
                if args.content_length:
                    url_data.content_length = domain.check_content_length()
                url_data.save()
                print(f'Data for URL {args.url} added successfully!')
        else:
            print("Error: Please specify either a single URL using '-u' or a file containing a list of URLs using '-l'.")

    elif args.action == 'remove':
        if args.url:
            url_data = UrlData.get(args.url)
            if url_data:
                url_data.remove()
                print(f'Data for URL {args.url} removed successfully!')
            else:
                print(f'Data for URL {args.url} not found!')
        else:
            print("Error: Please specify a URL using '-u' to remove its data.")

    # Additional functionality for getting all records
    elif args.subs:
        all_records_json = UrlData.get_all()
        print(all_records_json)

    elif args.logs:
        with open('log.txt') as file:
            data = file.readlines()
            for line in data:
                print(line.strip())


if __name__ == '__main__':
    main()
