from setuptools import setup

setup(
    name='URL_sentry',
    version='0.1',
    packages=['cli'],
    install_requires=[
        'rich',
        'requests',
        'python-decouple',
        'python-crontab',
    ],
    entry_points={
        'console_scripts': [
            'url-sentry=cli.cli:main',
        ],
    },
)
