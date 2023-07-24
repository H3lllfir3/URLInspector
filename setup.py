import os
from setuptools import setup
from setuptools.command.install import install
from crontab import CronTab


class CustomInstallCommand(install):
    def run(self):
        # Call the original install command first
        install.run(self)

        # Add the cronjob
        cron = CronTab(user=True)
        python_path = "/usr/bin/python3"  # Change this to the path of your Python executable
        job = cron.new(command=f'{python_path} {script_path}')
        job.hour.every(interval_hours)
        cron.write()

setup(
    name='URL_sentry',
    version='0.1',
    packages=['cli'],
    install_requires=[
        'rich',
        'requests',
        'python-dotenv',
        'python-crontab',
        'tldextract',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'url-sentry=cli.cli:main',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    }
)
