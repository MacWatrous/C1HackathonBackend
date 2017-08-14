from setuptools import setup

setup(
    name='c1-hackathon',
    packages=['c1-hackathon'],
    include_package_data=True,
    install_requires=[
        'flask', 'tweepy', 'textblob', 'json', 'psycopg2', 'time'
    ],
)