import logging
import unittest
from ..settings import database
from ..models.user import User
from ..models.evaluation import Evaluation
from ..models.contribution import Contribution


peewee_logger = logging.getLogger('peewee')


class TestCase(unittest.TestCase):
    """Base class for all tests"""
    db_tables = [User, Evaluation, Contribution]

    def setUp(self):
        # make peewee a bit more quiet
        peewee_logger.setLevel(logging.ERROR)
        # set up the database
        database.connect()
        database.create_tables(self.db_tables, safe=True)

    def tearDown(self):
        # reset the database
        database.drop_tables(self.db_tables)
        database.close()

    def reset_db(self):
        for table in self.db_tables:
            table.delete().execute()
