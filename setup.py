from setuptools import setup, find_packages
requires = [
    'sqlalchemy',
]

setup(
    name='backfeed-protocol',
    version='0.1',
    description='Implementation of the backfeed protocol',
    url='http://www.backfeed.cc/',
    author='Jelle Gerbrandy',
    author_email='jelle@gerbrandy.com',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    test_suite='backfeed_protocol',
    tests_require=requires,
    entry_points={"console_scripts": ["bfsim = backfeed_protocol.simulations.script:main", ]},
)
