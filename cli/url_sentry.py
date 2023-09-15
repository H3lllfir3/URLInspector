import hashlib
import os
from urllib.parse import urlparse, urljoin
import re

import requests
from bs4 import BeautifulSoup
import tldextract



class URLInspector:
    def __init__(self, url):
        self.url = self.add_scheme(url)
        self.save_directory = self.create_save_directory()
        self.BACK_LIST = [
            'jquery',
        ]
        self.response = self.fetch_response()

    def add_scheme(self, url):
        """
        Add a scheme (https://) to the URL if it doesn't have one.
        """
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme

        if not scheme:
            return "https://" + parsed_url.netloc + parsed_url.path.rstrip("/")

        return url.rstrip("/")

    def is_relative_url(self, url):
        """
        Check if a given URL is relative (doesn't have a domain).
        """
        parsed_url = urlparse(url)
        return not bool(parsed_url.netloc)

    def extract_site_name(self, url):
        extracted = tldextract.extract(url)
        return extracted.domain

    def create_save_directory(self):
        """
        Create a directory to save JS files based on the URL's hostname.
        """
        base_url = urlparse(self.url).hostname
        home_directory = os.path.expanduser("~")
        save_directory = os.path.join(home_directory, ".url_sentry", "js_files", base_url)
        os.makedirs(save_directory, exist_ok=True)
        return save_directory

    def fetch_response(self):
        """
        Fetch the URL's response, handling SSL errors by retrying with certificate verification disabled.
        """
        try:
            response = requests.get(self.url)
        except requests.exceptions.SSLError:
            response = requests.get(self.url, verify=False)

        return response

    def check_status_code(self):
        """
        Return the status code of the URL's response.
        """
        return self.response.status_code

    def check_content_length(self):
        """
        Return the content length of the URL's response.
        """
        return len(self.response.content)

    def check_title(self):
        """
        Extract the title from the HTML content of the URL's response.
        """
        soup = BeautifulSoup(self.response.text, 'html.parser')
        return soup.title.text.strip()

    def check_word_in_body(self, word):
        """
        Check if the given word is present in the body of the URL's response.
        """
        return word.lower() in self.response.text.lower()

    def check_js_files(self):
        """
        Check for blacklisted JS files in the URL's response, download and hash them, and save to a directory.
        """
        base_url = urlparse(self.url).hostname

        soup = BeautifulSoup(self.response.text, 'html.parser')
        js_tags = [script['src'] for script in soup.find_all('script', src=True)]

        js_modulepreload_links = soup.find_all('link', rel='modulepreload', href=re.compile(r'\.js$'))
        js_links = [link['href'] for link in js_modulepreload_links]

        all_js = js_links + js_tags

        base_url_path = f"{self.url}/"
        site_name = self.extract_site_name(self.url)
        base_domain_js_urls = [
            urljoin(base_url_path, js_url) if self.is_relative_url(js_url) else js_url
            for js_url in all_js
            if self.is_relative_url(js_url) or site_name in js_url
        ]
        
        base_domain_js_urls = [url.replace("//", "https://") if url.startswith("//") else url for url in base_domain_js_urls]

        js_hashes = []
        with requests.Session() as session:
            for js_url in base_domain_js_urls:
                if not any(blacklisted in js_url for blacklisted in self.BACK_LIST):
                    try:
                        js_response = session.get(js_url)
                        js_response.raise_for_status()  # Check for HTTP status code other than 200
                        js_hash = hashlib.md5(js_response.content).hexdigest()
                        js_filename = os.path.basename(js_url)
                        js_file_path = os.path.join(self.save_directory, f"{base_url}-{js_hash}.js")

                        with open(js_file_path, 'wb') as file:
                            file.write(js_response.content)

                        js_hashes.append(f'{js_url}|{js_hash}')
                    except requests.exceptions.RequestException as e:
                        print(f"Error fetching JS URL '{js_url}': {e}")

        return ','.join(js_hashes)