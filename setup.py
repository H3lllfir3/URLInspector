import os
from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
    
        install.run(self)

        from crontab import CronTab

        # Get the path of main.py relative to the setup.py file
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"main.py not found at '{script_path}'")


        cron = CronTab(user=True)
        python_path = "/usr/bin/python3"  # Change this to the path of your Python executable
        job = cron.new(command=f'{python_path} {script_path}')
        job.setall('0 * * * *') 
        cron.write()


setup(
    name='inspector',
    version='0.1',
    packages=['cli'],
    install_requires=[
        'rich',
        'requests',
        'python-dotenv',
        'python-crontab',
        'tldextract',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'inspector=cli.cli:main',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    }
)