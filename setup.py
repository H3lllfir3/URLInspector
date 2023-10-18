import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.install import install

from src.inspector.config import DB_URL
from src.inspector.db import create_db


create_db(DB_URL)


class CustomInstallCommand(install):
    def run(self):

        install.run(self)

        from crontab import CronTab

        # Get the path of main.py relative to the setup.py file
        script_path = Path(__file__).resolve().parent.joinpath('src', 'inspector', 'main.py')
        if not script_path.exists():
            raise FileNotFoundError(f"main.py not found at '{script_path}'")

        cron = CronTab(user=True)

        python_path = sys.executable
        job = cron.new(command=f'{python_path} {script_path}')
        job.setall('0 * * * *')
        cron.write()


setup(
    name='inspector',
    version='0.1',
    packages=['inspector'],
    install_requires=[
        'rich==13.5.3',
        'requests==2.31.0',
        'python-dotenv==1.0.0',
        'python-crontab==3.0.0',
        'tldextract==3.6.0',
        'beautifulsoup4==4.12.2',
        'validators==0.22.0',
    ],
    entry_points={
        'console_scripts': [
            'inspector=src.inspector.cli:main',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
)
