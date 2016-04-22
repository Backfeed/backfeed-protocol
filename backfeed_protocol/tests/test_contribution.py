from ..contracts.dmag import DMagContract

from test_contract_base import BaseContractTestCase


class ContributionTest(BaseContractTestCase):
    """test dmag protocol"""
    contract_class_to_test = DMagContract

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
        self.user1 = contract.get_user(user1)
        self.user2 = contract.get_user(user2)
        self.user3 = contract.get_user(user3)

    def test_contribution_statistics(self):
        # set up an interesting situation
        self.get_contract_with_data()

        stats = self.contribution0.get_statistics()
        self.assertEqual(stats['evaluations'][1]['reputation'], self.user1.reputation + self.user2.reputation)
        self.assertEqual(stats['evaluations'][0]['reputation'], self.user3.reputation)
