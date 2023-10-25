import logging
import os
from pathlib import Path


HOME = Path.home()
BASE_DIR = HOME / '.inspector'
DB_PATH = BASE_DIR / 'data.db'
DB_URL = f'sqlite:///{DB_PATH}'
LOG_FILE = BASE_DIR / 'app.log'
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL') or 'put your webhook url here'


if not BASE_DIR.exists():
    BASE_DIR.mkdir()


def get_logger():

    logger = logging.getLogger('inspector')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)

    return logger
