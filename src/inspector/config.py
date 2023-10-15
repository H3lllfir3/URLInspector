import logging
from pathlib import Path


HOME = Path.home()
BASE_DIR = HOME / '.inspector'
DB_URL = 'sqlite:///data.db'
LOG_FILE = BASE_DIR / 'app.log'

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
