import unittest
from backfeed_protocol import utils


class TestCase(unittest.TestCase):
    """Base class for all tests"""
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:',
    }

    def setUp(self):
        # set up the database
        utils.setup_database(settings=self.settings)

    def tearDown(self):
        utils.reset_database()
