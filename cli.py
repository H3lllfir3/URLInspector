import json
import argparse
from orm import UrlData
from url_sentry import URL


parser = argparse.ArgumentParser(description='URL Data Management')
parser.add_argument('action', nargs='?', choices=['add', 'remove'], help='Action to perform: add or remove')
parser.add_argument('-u', '--url', help='URL of the data')
parser.add_argument('-status-code', action='store_true', help='Include status code')
parser.add_argument('-title', action='store_true', help='Include title')
parser.add_argument('-js', action='store_true', help='Include JS')
parser.add_argument('-subs', action='store_true', help='Include all records')
parser.add_argument('-content-length', action='store_true', help='Include content length')
parser.add_argument('-body', action='store_true', help='Content of the body')


args = parser.parse_args()

if args.action == 'add':
    url_data = UrlData(url=args.url)
    domain = URL(args.url)

    if args.status_code:
        url_data.status_code = domain.check_status_code()

    if args.title:
        url_data.title = domain.check_title()

    if args.js:
        url_data.js_file = domain.check_js_files() 
    
    if args.content_length:
        url_data.content_length = domain.check_content_length()

    url_data.save()
    print('Data added successfully!')

elif args.action == 'remove':
    url_data = UrlData.get(args.url)
    if url_data:
        url_data.remove()
        print('Data removed successfully!')
    else:
        print('Data not found!')

# Additional functionality for getting all records
if args.subs:
    all_records_json = UrlData.get_all()
    print(all_records_json)
