from setuptools import setup

setup(
    name='backfeed-protocol',
    version='0.1',
    description='Implementation of the backfeed protocol',
    url='http://www.backfeed.cc/',
    author='Jelle Gerbrandy',
    author_email='jelle@gerbrandy.com',
    license='GPL',
    packages=['protocol'],
    install_requires=[
        'peewe',
    ],
    zip_safe=False,
)
