import types

from common import TestCase

from ..contracts.base import BaseContract
from .. import utils


class BaseContractTestCase(TestCase):
    """test general functionality of a contract

    TestCases for new contracts should inherit from this class
    """

    contract_class_to_test = BaseContract

    def setUp(self):
        super(BaseContractTestCase, self).setUp()
        self.contract = self.get_fresh_contract()
        self.allowedDeviation = 0.00005

    def get_fresh_contract(self):
        """get a contract with default settings but without users or other data"""
        utils.reset_database()
        return self.contract_class_to_test()


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
        contribution1 = contract.create_contribution(user=user1)

        # we can retrieve the contribution from the contract
        self.assertEqual(contract.get_contributions(), [contribution1])

        # user2 evaluates the contribution
        value = 1.0
        evaluation1 = contract.create_evaluation(user1, contribution1, value=value)

        self.assertEqual(contract.get_evaluations(), [evaluation1])
        self.assertEqual(evaluation1.user, user1)
        self.assertEqual(evaluation1.contribution, contribution1)
        self.assertEqual(evaluation1.value, value)

    def test_delete_users(self):
        self.contract.create_user()
        self.contract.create_user()
        self.assertEqual(self.contract.get_users().count(), 2)
        self.contract.delete_users()
        self.assertEqual(self.contract.get_users().count(), 0)

    def test_get_contribution(self):
        user = self.contract.create_user()
        contribution1 = self.contract.create_contribution(user=user)
        self.assertEqual(self.contract.get_contribution(contribution1), contribution1)
