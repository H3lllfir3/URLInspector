import os
from setuptools import setup
from setuptools.command.install import install
from crontab import CronTab

class CustomInstallCommand(install):
    def run(self):
        # Call the original install command first
        install.run(self)

        # Define the cronjob details
        script_path = os.path.join(os.path.abspath("main.py"))
        interval_minutes = 5  # Replace with the desired interval in minutes (1 hour in this case)

        # Add the cronjob
        cron = CronTab(user=True)
        job = cron.new(command=f'python3 {script_path}')
        job.minute.every(interval_minutes)
        cron.write()

setup(
    name='URL_sentry',
    version='0.1',
    packages=['cli'],
    install_requires=[
        'rich',
        'requests',
        'python-decouple'
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
