import types
import datetime

from common import TestCase
from ..contracts.base import BaseContract
from .. import utils
from ..models import DBSession
from ..models import with_session


class BaseContractTestCase(TestCase):
    """test general functionality of a contract

    TestCases for new contracts should inherit from this class
    """

    contract_class_to_test = BaseContract

    def setUp(self):
        super(BaseContractTestCase, self).setUp()
        self.contract = self.get_fresh_contract()
        self.allowedDeviation = 0.00005

    @with_session
    def get_fresh_contract(self):
        """get a contract with default settings but without users or other data"""
        utils.reset_database()
        contract = self.contract_class_to_test()
        DBSession.add(contract)
        return contract

    def get_contract_with_data(self):
        contract = self.get_fresh_contract()

        user0 = contract.create_user()
        user1 = contract.create_user()
        user2 = contract.create_user()
        user3 = contract.create_user()

        contribution0 = contract.create_contribution(user=user0)
        contribution1 = contract.create_contribution(user=user0)
        contribution2 = contract.create_contribution(user=user1)

        contract.create_evaluation(contribution=contribution0, user=user1, value=1)
        contract.create_evaluation(contribution=contribution0, user=user2, value=1)
        contract.create_evaluation(contribution=contribution0, user=user3, value=0)
        contract.create_evaluation(contribution=contribution1, user=user2, value=1)
        contract.create_evaluation(contribution=contribution1, user=user3, value=1)

        self.contribution0 = contribution0
        self.contribution1 = contribution1
        self.contribution2 = contribution2
        self.user0 = user0
        self.user1 = user1
        self.user2 = user2
        self.user3 = user3
        return contract


class ContractSanityTest(BaseContractTestCase):
    """Basic tests that every contract should pass"""

    def test_sanity(self):
        """We follow a typical workflow without checking the exact values
        to check if everything works"""

        contract = self.contract
        # we setup the contract with 2 user
        user1 = contract.create_user()
        user2 = contract.create_user()

        # we should now have 2 users
        self.assertEqual(contract.get_users(), [user1, user2])

        # a user has a reputation and a number of tokens
        self.assertTrue(isinstance(user1.reputation, types.FloatType))
        self.assertTrue(isinstance(user1.tokens, types.FloatType))

        # user1 makes a contribution
        self.assertEqual(contract.get_contributions(), [])
        contribution1 = contract.create_contribution(user=user1)
        self.assertEqual(contract.get_contributions(), [contribution1])
        contribution2 = contract.create_contribution(user=user2)
        self.assertEqual(contract.get_contributions(), [contribution1, contribution2])

        # we can retrieve the contribution from the contract
        self.assertEqual(contract.get_contributions(), [contribution1, contribution2])

        # user2 evaluates the contribution
        value = 1.0
        evaluation1 = contract.create_evaluation(user1, contribution1, value=value)

        self.assertEqual(contract.get_evaluations(), [evaluation1])
        self.assertEqual(evaluation1.user, user1)
        self.assertEqual(evaluation1.contribution, contribution1)
        self.assertEqual(evaluation1.value, value)

        contract.create_evaluation(user1, contribution2, value=1)
        contract.create_evaluation(user2, contribution2, value=0)

        self.assertRaises(ValueError, contract.create_evaluation, user2, contribution1, value=3.14)

    def test_get_user(self):
        user_id = self.contract.create_user().id
        user = self.contract.get_user(user_id=user_id)

        self.assertEqual(user.id, user_id)
        self.assertTrue(isinstance(user.time, datetime.datetime))
