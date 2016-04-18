import types
import datetime

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
        contract = self.contract_class_to_test()
        contract.save()
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

    # def test_delete_users(self):
    #     self.contract.create_user()
    #     self.contract.create_user()
    #     self.assertEqual(self.contract.get_users().count(), 2)
    #     self.contract.delete_users()
    #     self.assertEqual(self.contract.get_users().count(), 0)

    def test_get_contribution(self):
        user = self.contract.create_user()
        contribution_id = self.contract.create_contribution(user=user).id
        contribution = self.contract.get_contribution(contribution_id=contribution_id)

        self.assertEqual(contribution.id, contribution_id)
        self.assertEqual(contribution.user, user)
        self.assertTrue(isinstance(contribution.time, datetime.datetime))

    def test_get_user(self):
        user_id = self.contract.create_user().id
        user = self.contract.get_user(user_id=user_id)

        self.assertEqual(user.id, user_id)
        self.assertTrue(isinstance(user.time, datetime.datetime))

    def test_get_evaluation(self):
        user = self.contract.create_user()
        contribution = self.contract.create_contribution(user=user)
        value = 3.14
        evaluation_id = self.contract.create_evaluation(contribution=contribution, user=user, value=value).id

        evaluation = self.contract.get_evaluation(evaluation_id)

        self.assertEqual(evaluation.id, evaluation_id)
        self.assertEqual(evaluation.user, user)
        self.assertEqual(evaluation.contribution, contribution)
        self.assertEqual(evaluation.value, value)
        self.assertTrue(isinstance(evaluation.time, datetime.datetime))
