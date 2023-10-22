import argparse
import os
from typing import List
from urllib.parse import urlparse

from rich import print
from tqdm import tqdm

from .config import DB_URL
from .config import get_logger
from .config import LOG_FILE
from .db import get_session
from .models import UrlData
from .queries import UrlDataQueries
from .urlinspector import URLInspector


logger = get_logger()


def validate_url(url: str) -> bool:
    """Validate URL input"""
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


def validate_file(fil_path: str) -> bool:
    """Validate file exists"""
    return os.path.exists(fil_path)


def get_urls_from_file(file_path: str) -> List[str]:
    """Extract URLs from file"""
    with open(file_path) as f:
        urls = [line.strip() for line in f]
        return [url for url in urls if validate_url(url)]


def get_inspector(url: str) -> URLInspector:
    return URLInspector(url)


def main():
    """Manage URL Data monitoring using CLI."""

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
        'status-code', action='store_true',
        help='Include status code',
    )
    parser.add_argument('title', action='store_true', help='Include title')
    parser.add_argument('js', action='store_true', help='Include JS')
    parser.add_argument(
        'subs', action='store_true',
        help='Include all records',
    )
    parser.add_argument(
        '-content-length', action='store_true',
        help='Include content length',
    )

    parser.add_argument('logs', action='store_true', help='Show logs')

    args = parser.parse_args()

    # get the db session
    session = get_session(DB_URL)
    queries = UrlDataQueries(session)

    if args.action == 'add':
        if args.list:
            urls = get_urls_from_file(args.list)

            for url in tqdm(urls):
                url_data = queries.get(url)
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

                    queries.add(url_data)
                    print(f'Data for URL {url} updated successfully!')
                else:
                    url_data = queries.get(url)
                    domain = get_inspector(url)
                    if args.status_code:
                        url_data.status_code = domain.check_status_code()
                    if args.title:
                        url_data.title = domain.check_title()
                    if args.js:
                        url_data.js_hash = domain.check_js_files()
                    if args.content_length:
                        url_data.content_length = domain.check_content_length()

                    queries.add(url_data)
                    print(f'Data for URL {url} added successfully!')

        elif args.url:
            url_data = queries.get(args.url)
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

                queries.update(url_data)
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

                queries.add(url_data)
                print(f'Data for URL {args.url} added successfully!')
        else:
            print("Error: Please specify either a single URL using '-u' or a file containing a list of URLs using '-l'.")

    elif args.action == 'remove':
        if args.url:
            url_data = queries.delete(args.url)
            if url_data:

                print(f'Data for URL {args.url} removed successfully!')
            else:
                print(f'Data for URL {args.url} not found!')
        else:
            print("Error: Please specify a URL using '-u' to remove its data.")

    elif args.subs:
        all_records_json = queries.get_all()
        print(all_records_json)

    elif args.logs:
        with open(LOG_FILE) as file:
            data = file.readlines()
            for line in data:
                print(line.strip())


if __name__ == '__main__':
    main()
