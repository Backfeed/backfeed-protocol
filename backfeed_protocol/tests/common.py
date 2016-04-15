import logging
import unittest
from ..settings import database
from backfeed_protocol import utils


peewee_logger = logging.getLogger('peewee')


class TestCase(unittest.TestCase):
    """Base class for all tests"""

    def setUp(self):
        # make peewee a bit more quiet
        peewee_logger.setLevel(logging.ERROR)
        # set up the database
        utils.setup_database()

    def tearDown(self):
        # reset the database
        utils.reset_database()
        database.close()
