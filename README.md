# URL Sentry - URL Monitoring and Management CLI

This is a Python CLI tool for managing URL data, including status code, title, JS files, content length, and more. It allows you to add, remove, and view URL data in a simple and convenient way.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/H3lllfir3/URL_Sentry.git
cd URL_Sentry
```

2. Install the CLI globally:

```bash
pip install -e .
```

3. Scheduling `main.py` Using a Cron Job:

a. Open the crontab for editing:
Run the following command to open the crontab for editing:

```bash
crontab -e
```
b. Add the cron job to run main.py every hour

Add the following line at the end of the crontab file:

```bash
0 * * * * /path/to/python /path/to/main.py
```
Make sure to replace /path/to/python with the absolute path to your Python executable and /path/to/main.py with the absolute path to your main.py file.

4. Sending Notifications.

To enable notifications for important events, you need to set up a Discord webhook URL. Store your Discord webhook URL in the `.env` file at the root of the project as follows:

```plaintext
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
```

## Usage

### Add URL Data

To add URL data, use the following command:

```bash
url-sentry add -u <url> [options]
```

Available options:
- `-status-code`: Include status code.
- `-title`: Include title.
- `-js`: Include JS files.
- `-content-length`: Include content length.

Examples:
```bash
url-sentry add -u domain.tld -content-length
url-sentry add -u domain.tld -title
url-sentry add -u domain.tld -status-code -js
```

### Remove URL Data

To remove URL data, use the following command:

Example:
```bash
url-sentry remove -u domain.tld
```

### View Logs

To view the logs, use the following command:

```bash
url-sentry -logs
```

### View All Records

To view all URL records, use the following command:

```bash
url-sentry -subs | jq
```


## Contributing

Contributions are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to use, modify, and distribute this code for personal and commercial use.
