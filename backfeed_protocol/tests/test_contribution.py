from datetime import datetime
from ..contracts.dmag import DMagContract

from test_contract_base import BaseContractTestCase


class ContributionTest(BaseContractTestCase):
    """test dmag protocol"""
    contract_class_to_test = DMagContract

    def test_contribution_statistics(self):
        # set up an interesting situation
        self.get_contract_with_data()

        stats = self.contribution0.get_statistics()
        self.assertEqual(stats['evaluations'][1]['reputation'], self.user1.reputation + self.user2.reputation)
        self.assertEqual(stats['evaluations'][0]['reputation'], self.user3.reputation)

    def test_create_distribution_errors(self):
        # test contribution type and error
        contract = self.contract
        user = contract.create_user()
        self.assertRaises(KeyError, contract.create_contribution, user, contribution_type='spam')

    def test_get_contribution(self):
        user = self.contract.create_user()
        contribution = self.contract.create_contribution(user=user)
        contribution_id = contribution.id
        contribution = self.contract.get_contribution(contribution_id=contribution_id)

        self.assertEqual(contribution.id, contribution_id)
        self.assertEqual(contribution.user, user)
        self.assertTrue(isinstance(contribution.time, datetime))

    def test_contribution_score(self):
        contract = self.get_contract_with_data()
        contribution = self.contribution0

        score_at_time0 = contract.contribution_score(contribution)
        contribution.time = datetime(2000, 1, 1)
        score_at_time1 = contract.contribution_score(contribution)
        self.assertLess(score_at_time1, score_at_time0)

    def test_contribution_engaged_reputation(self):
        self.get_contract_with_data()
        self.assertEqual(self.contribution0.engaged_reputation(), self.user1.reputation + self.user2.reputation + self.user3.reputation)
        self.assertEqual(self.contribution1.engaged_reputation(), self.user2.reputation + self.user3.reputation)
