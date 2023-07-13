from orm import UrlData
from url_sentry import URL
import json


def main():
    all_records_json = json.loads(UrlData.get_all())
    
    for record in all_records_json:
        data = {i:j for i,j in record.items() if j is not None}
        domain = URL(data['url'])
        if data['status_code']:
            if domain.check_status_code() != data['status_code']:
                print(f"Status code changed for {data['url']}")
        if data['title']:
            if domain.check_title() != data['title']:
                print(f"Title changed for {data['url']}")
        if data['body']:
            if domain.check_word_in_body(data['body']):
                print(f"Word '{data['body']}' founded in body for {data['url']}")
        
        if data['content_length']:
            if domain.check_content_length() != data['content_length']:
                print(f"Content length changed for {data['url']}")
        
        if data['js_file']:
            if domain.check_js_files(data['js_file']):
                print(f"JS file changed for {data['url']}")

main()