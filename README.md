# URL Inspector - URL Monitoring and Management CLI

- "URL Inspector" is a Python CLI tool for monitoring website data, including status code, title, JS files, and content length.
- It allows users to add, remove, and view URL data in a simple and convenient way.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/H3lllfir3/URLInspector.git
cd URLInspector
```

2. Sending Notifications:

- Users can enable notifications for important events by setting up a Discord webhook URL.
```python
# Put the webhook URL in src/inspector/config.py as follows:
DISCORD_WEBHOOK_URL = "your_webhook_url_here"
```

3. Install the CLI globally:

```bash
pip3 install -r requirements.txt
python3 setup.py install
```


### Scheduling Using a Cron Job

- The script runs automatically every 1 hour.


### Usage

#### Add URL Data

To add URL data, use the following command:

```bash
inspector add -u <url> [options]
```

Available options:
- `-status-code`: Include status code.
- `-title`: Include title.
- `-js`: Include JS files.
- `-content-length`: Include content length.

Examples:

```bash
inspector add -u domain.tld -content-length
inspector add -u domain.tld -title
inspector add -u domain.tld -status-code -js
```

#### Remove URL Data

To remove URL data, use the following command:

```bash
inspector remove -u domain.tld
```

#### View Logs

To view the logs, use the following command:

```bash
inspector -logs
```

#### View All Records

To view all URL records, use the following command:

```bash
inspector -subs
```

### Contributing

- Contributions are welcome! Users can open issues or submit pull requests for bug fixes or improvements.

### License

- This project is licensed under the MIT License, allowing free use, modification, and distribution for personal and commercial purposes.
