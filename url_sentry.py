import argparse
import requests
import hashlib
import time
import sqlite3
import yaml


def send_notification(message):
    # Send notification using Discord webhook or any other method
    print(message)


def store_data(url, data):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS data (url TEXT, status_code INTEGER, content_length INTEGER, title TEXT, js_hash TEXT)")
    c.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()


def check_status_code(url):
    response = requests.get(url)
    return response.status_code


def check_content_length(url):
    response = requests.get(url)
    return len(response.content)


def check_title(url):
    response = requests.get(url)
    return response.text.split('<title>')[1].split('</title>')[0]


def check_word_in_body(url, word):
    response = requests.get(url)
    return word.lower() in response.text.lower()


def check_js_file(url):
    response = requests.get(url)
    js_urls = []  # Extract JavaScript URLs from response.text
    for js_url in js_urls:
        js_response = requests.get(js_url)
        js_hash = hashlib.md5(js_response.content).hexdigest()
        # Compare js_hash with the previous hash in the database
        # If it's different, send a notification and update the stored hash in the database


def parse_arguments():
    parser = argparse.ArgumentParser(description='URL Monitoring')
    parser.add_argument('-u', '--url', help='URL to monitor')
    parser.add_argument('-list', '--url-list', help='File containing a list of URLs to monitor')
    parser.add_argument('-status-code', action='store_true', help='Monitor status code')
    parser.add_argument('-content-length', action='store_true', help='Monitor content length')
    parser.add_argument('-title', action='store_true', help='Monitor title')
    parser.add_argument('-body', type=str, help='Word to monitor in the body')
    parser.add_argument('-js', action='store_true', help='Monitor JavaScript files')
    parser.add_argument('-time', type=int, default=60, help='Monitoring time interval in minutes')
    return parser.parse_args()


def load_config():
    with open('~/.tomonitor/config.yaml') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config


def main():
    args = parse_arguments()
    config = load_config()
    url = args.url
    urls = []

    if args.url_list:
        with open(args.url_list) as f:
            urls = f.read().splitlines()

    while True:
        for u in urls:
            data = [u, None, None, None, None]
            if args.status_code:
                data[1] = check_status_code(u)
            if args.content_length:
                data[2] = check_content_length(u)
            if args.title:
                data[3] = check_title(u)
            if args.body:
                if check_word_in_body(u, args.body):
                    send_notification(f"DATA TIME\nThe word '{args.body}' was found at {u}.")
            if args.js:
                check_js_file(u)
            if data[1:] != [None, None, None, None]:
                stored_data = retrieve_stored_data(u)
                if stored_data:
                    if data[1:] != stored_data[1:]:
                        # Changes detected, send notification
                        send_notification(format_data_changes(data, stored_data))
                store_data(u, data)
        time.sleep(args.time * 60)


if __name__ == '__main__':
    main()
