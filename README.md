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
python3 cli.py add -u <url> [options]
```

Available options:
- `-status-code`: Include status code.
- `-title`: Include title.
- `-js`: Include JS files.
- `-content-length`: Include content length.

Examples:
```bash
python3 cli.py add -u h3llfir3.xyz -content-length
python3 cli.py add -u h3llfir3.xyz -title
python3 cli.py add -u h3llfir3.xyz -status-code -js
```

### Remove URL Data

To remove URL data, use the following command:

```bash
python3 cli.py remove -u <url>
```

Example:
```bash
python3 cli.py remove -u h3llfir3.xyz
```

### View Logs

To view the logs, use the following command:

```bash
python3 cli.py -logs
```

### View All Records

To view all URL records, use the following command:

```bash
python3 cli.py -subs | jq
```

The output will be formatted using `jq` for better readability.

## Dependencies

- `rich`: A library for beautiful and interactive terminal output.
- `requests`: A library for making HTTP requests.

## Contributing

Contributions are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to use, modify, and distribute this code for personal and commercial use.

---
With this README.md, you provide an overview of your URL Data Management CLI, its usage, and how to get started. Customize the installation and usage instructions based on your specific implementation details. Make sure to update the `<url>` placeholder with appropriate URLs and replace `your_username` with your GitHub username in the installation section.