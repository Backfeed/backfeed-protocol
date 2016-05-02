import sqlalchemy
import logging

from test_contract_base import BaseContractTestCase
from ..models import DBSession
from ..models.user import User
from ..models.contribution import Contribution
from ..models.evaluation import Evaluation


class TestWithPostgres(BaseContractTestCase):
    """All the other tests run in memory - here we test with files"""

    settings = {
        'sqlalchemy.url': 'postgresql://backfeed-test:backfeed@localhost:5432/backfeed-test',
    }

    def setUp(self):

        try:
            super(TestWithPostgres, self).setUp()
            self.db_ok = True
        except sqlalchemy.exc.OperationalError as error:
            msg = ''
            msg += '\n'
            msg += '*' * 80
            msg += '\n'
            msg += "WARNING: There was an error connecting to the postgres server."
            msg += '\n'
            msg += "For this test to work, you need to set up a test database"
            msg += '\n'
            msg += self.settings['sqlalchemy.url']
            msg += '\n'
            msg += 'See the CONTRIBUTING file for details'
            msg += '\n'
            msg += unicode(error)
            msg += '\n'
            msg += '*' * 80
            self.db_ok = False
            logging.error(msg)

    def test_sanity(self):
        # the connection is made and defined in self.setUp
        if self.db_ok:
            self.assertTrue(self.contract.create_user())

    def test_persistence(self):
        """test if data is really really saved in the database"""
        user = self.contract.create_user()
        contribution = self.contract.create_contribution(user=user)
        self.contract.create_evaluation(user=user, contribution=contribution, value=1)
        self.assertEqual(DBSession.query(User).count(), 1)
        self.assertEqual(DBSession.query(Contribution).count(), 1)
        self.assertEqual(DBSession.query(Evaluation).count(), 1)
        DBSession.close()
        self.assertEqual(DBSession.query(User).count(), 1)
        self.assertEqual(DBSession.query(Contribution).count(), 1)
        self.assertEqual(DBSession.query(Evaluation).count(), 1)
