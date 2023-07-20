# URL Data Management CLI

This is a Python CLI tool for managing URL data, including status code, title, JS files, content length, and more. It allows you to add, remove, and view URL data in a simple and convenient way.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/url-data-management-cli.git
cd url-data-management-cli
```

2. Install the CLI globally:

```bash
pip install -e .
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
url-sentry add -u h3llfir3.xyz -content-length
url-sentry add -u h3llfir3.xyz -title
url-sentry add -u h3llfir3.xyz -status-code -js
```

### Remove URL Data

To remove URL data, use the following command:

```bash
url-sentry remove -u <url>
```

Example:
```bash
url-sentry remove -u h3llfir3.xyz
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

The output will be formatted using `jq` for better readability.

### Setting Discord Webhook

To enable notifications for important events, you need to set up a Discord webhook URL. Store your Discord webhook URL in the `.env` file at the root of the project as follows:

```plaintext
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
```

The CLI will read this URL from the environment variable and use it to send notifications.

## Dependencies

- `rich`: A library for beautiful and interactive terminal output.
- `requests`: A library for making HTTP requests.
- `decouple`: A library to get environment variables.

## Contributing

Contributions are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to use, modify, and distribute this code for personal and commercial use.

---

With this README.md, you provide an overview of your URL Data Management CLI, its usage, and how to get started. Customize the installation and usage instructions based on your specific implementation details. Make sure to update the `<url>` placeholder with appropriate URLs, replace `your_username` with your GitHub username in the installation section, and inform users to set up their Discord webhook URL in the `.env` file.