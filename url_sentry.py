import hashlib
import os
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup


class URL:
    def __init__(self, url):
        self.url = self.add_scheme(url)
        self.save_directory = self.create_save_directory()

    def add_scheme(self, url):
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme

        if not scheme:
            return "https://" + parsed_url.netloc + parsed_url.path.rstrip("/")
        
        return url.rstrip("/")

    def is_relative_url(self, url):
        parsed_url = urlparse(url)
        return not bool(parsed_url.netloc)

    def create_save_directory(self):
        base_url = urlparse(self.url).hostname
        home_directory = os.path.expanduser("~")
        save_directory = os.path.join(home_directory, ".url_sentry", "js_files", base_url)
        os.makedirs(save_directory, exist_ok=True)
        return save_directory

    def check_status_code(self):
        response = requests.get(self.url)
        return response.status_code

    def check_content_length(self):
        response = requests.get(self.url)
        return len(response.content)

    def check_title(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.title.text.strip()

    def check_word_in_body(self, word):
        response = requests.get(self.url)
        return word.lower() in response.text.lower()

    def check_js_files(self, save_directory):
        response = requests.get(self.url)
        base_url = urlparse(self.url).hostname

        soup = BeautifulSoup(response.text, 'html.parser')
        js_urls = [script['src'] for script in soup.find_all('script', src=True)]

        base_url_path = f"{base_url}/"
        base_domain_js_urls = [
            urljoin(base_url, js_url) if self.is_relative_url(js_url) else js_url
            for js_url in js_urls
            if self.is_relative_url(js_url) or base_url in js_url
        ]
        
        absolute_urls = [urljoin(self.url, url) for url in base_domain_js_urls]
        js_hashes = []

        for js_url in absolute_urls:
            js_response = requests.get(js_url)
            js_hash = hashlib.md5(js_response.content).hexdigest()

            js_filename = os.path.basename(js_url)
            js_file_path = os.path.join(save_directory, f"{base_url}-{js_hash}.js")

            with open(js_file_path, 'wb') as file:
                file.write(js_response.content)

            js_hashes.append(f'{js_url}|{js_hash}')

        return ','.join(js_hashes)

