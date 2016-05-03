from datetime import datetime
from ..contracts.dmag import DMagContract

from test_contract_base import BaseContractTestCase


class EvaluationTest(BaseContractTestCase):
    """test dmag protocol"""
    contract_class_to_test = DMagContract
    contract_name = u'dmag'

    def test_get_evaluation(self):
        user = self.contract.create_user(reputation=3.141)
        contribution = self.contract.create_contribution(user=user)
        value = 1
        evaluation = self.contract.create_evaluation(contribution=contribution, user=user, value=value)

        evaluation = self.contract.get_evaluation(evaluation.id)

        self.assertEqual(evaluation.id, evaluation.id)
        self.assertEqual(evaluation.user, user)
        self.assertEqual(evaluation.contribution, contribution)
        self.assertEqual(evaluation.value, value)
        self.assertTrue(isinstance(evaluation.time, datetime))

    def test_get_evaluations(self):
        contract = self.get_contract_with_data()

        self.assertEqual(len(contract.get_evaluations(value=1)), 4)
        self.assertEqual(len(contract.get_evaluations(value=0)), 1)
        self.assertEqual(len(contract.get_evaluations(value=0)), 1)
        self.assertEqual(len(contract.get_evaluations(contribution_id=self.contribution0.id)), 3)
        self.assertEqual(len(contract.get_evaluations(contribution_id=self.contribution1.id)), 2)
        self.assertEqual(len(contract.get_evaluations(contribution_id=self.contribution2.id)), 0)
        self.assertEqual(len(contract.get_evaluations(evaluator_id=self.user0.id)), 0)
        self.assertEqual(len(contract.get_evaluations(evaluator_id=self.user1.id)), 1)
        self.assertEqual(len(contract.get_evaluations(evaluator_id=self.user2.id)), 2)
        self.assertEqual(len(contract.get_evaluations(evaluator_id=self.user3.id)), 2)

    def test_token_rewards_for_evaluators(self):
        contract = self.get_fresh_contract()
        contract.REWARD_TOKENS_TO_EVALUATORS = True

        user0 = contract.create_user(reputation=3.141)
        user1 = contract.create_user(reputation=3.141)
        user2 = contract.create_user(reputation=3.141)
        user3 = contract.create_user(reputation=3.141)
        user4 = contract.create_user(reputation=3.141)

        contribution0 = contract.create_contribution(user=user0)
        contract.create_evaluation(user1, contribution0, value=1)
        self.assertEqual(user1.tokens, contract.USER_INITIAL_TOKENS + 0.2 * contract.CONTRIBUTION_TYPE[contribution0.contribution_type]['fee'])
        contract.create_evaluation(user2, contribution0, value=0)
        self.assertEqual(user2.tokens, contract.USER_INITIAL_TOKENS + 0.2 * contract.CONTRIBUTION_TYPE[contribution0.contribution_type]['fee'])
        contract.create_evaluation(user3, contribution0, value=1)
        self.assertEqual(user3.tokens, contract.USER_INITIAL_TOKENS + 0.2 * contract.CONTRIBUTION_TYPE[contribution0.contribution_type]['fee'])
        contract.create_evaluation(user4, contribution0, value=0)
        self.assertEqual(user4.tokens, contract.USER_INITIAL_TOKENS + 0.2 * contract.CONTRIBUTION_TYPE[contribution0.contribution_type]['fee'])

        # check token balance unchanged when voting again
        contract.create_evaluation(user1, contribution0, value=0)
        self.assertEqual(user1.tokens, contract.USER_INITIAL_TOKENS + 0.2 * contract.CONTRIBUTION_TYPE[contribution0.contribution_type]['fee'])

    def test_vote_changing_fee(self):
        # we compare two scenarios: a user changes her vote up-down-up
        # versus the user just voting up once
        initial_reputation = 10
        contract = self.contract
        user = contract.create_user(reputation=initial_reputation)
        contributor = contract.create_user(reputation=20)
        contribution = contract.create_contribution(user=contributor)

        user.reputation = initial_reputation
        contract.create_evaluation(contribution=contribution, user=user, value=1)
        fee_paid = initial_reputation - user.reputation

        contract.create_evaluation(contribution=contribution, user=user, value=0)

        # we want to compare the fee of the first vote with this third vote
        # the fee should be the same
        user.reputation = initial_reputation
        contract.create_evaluation(contribution=contribution, user=user, value=1)
        self.assertEqual(fee_paid, initial_reputation - user.reputation)

    def test_vote_changing_removes_previous_evaluations(self):
        contract = self.contract
        user0 = contract.create_user(tokens=10, reputation=10)
        contribution0 = contract.create_contribution(user=user0)
        contract.create_evaluation(contribution=contribution0, user=user0, value=1)
        contract.create_evaluation(contribution=contribution0, user=user0, value=1)
        contract.create_evaluation(contribution=contribution0, user=user0, value=0)
        self.assertEqual(len(contribution0.evaluations), 1)

    def test_vote_changing_attack1(self):
        contract = self.contract

        user0 = contract.create_user(tokens=10, reputation=10)
        user1 = contract.create_user(tokens=10, reputation=10)
        user2 = contract.create_user(tokens=10, reputation=20)
        user3 = contract.create_user(tokens=10, reputation=10)  # NOQA
        user4 = contract.create_user(tokens=10, reputation=10)  # NOQA
        contract.create_user(tokens=10, reputation=10)
        contract.create_user(tokens=10, reputation=10)

        contribution0 = contract.create_contribution(user=user0)

        contract.create_evaluation(contribution=contribution0, user=user1, value=1)
        contract.create_evaluation(contribution=contribution0, user=user2, value=1)

        old_stats = contribution0.get_statistics()

        # we have user1 change his vote to 0, and then to 1 again
        contract.create_evaluation(contribution=contribution0, user=user1, value=0)
        contract.create_evaluation(contribution=contribution0, user=user1, value=1)

        # now we expect both the score as the engaged_reputation to be lower than before
        new_stats = contribution0.get_statistics()

        # the score is NOT LOWER
        self.assertGreater(new_stats['score'], old_stats['score'])
        self.assertGreater(new_stats['engaged_reputation_normal'], old_stats['engaged_reputation_normal'])

    def test_vote_changing_score_attack2(self):
        contract = self.contract

        user0 = contract.create_user(tokens=10, reputation=10)
        user1 = contract.create_user(tokens=10, reputation=10)
        user2 = contract.create_user(tokens=10, reputation=10)
        user3 = contract.create_user(tokens=10, reputation=10)
        user4 = contract.create_user(tokens=10, reputation=10)
        user5 = contract.create_user(tokens=10, reputation=10)  # NOQA
        user6 = contract.create_user(tokens=10, reputation=10)  # NOQA

        contribution0 = contract.create_contribution(user=user1)

        contract.create_evaluation(contribution=contribution0, user=user0, value=1)
        contract.create_evaluation(contribution=contribution0, user=user1, value=1)
        contract.create_evaluation(contribution=contribution0, user=user2, value=1)
        contract.create_evaluation(contribution=contribution0, user=user3, value=1)
        contract.create_evaluation(contribution=contribution0, user=user4, value=1)

        # simulate an attack by user1 and user2 changing their votes
        original_rep = user1.relative_reputation() + user2.relative_reputation()

        # user1 and user2 vote alternately
        contract.create_evaluation(contribution=contribution0, user=user1, value=0)
        contract.create_evaluation(contribution=contribution0, user=user2, value=0)
        contract.create_evaluation(contribution=contribution0, user=user1, value=1)
        contract.create_evaluation(contribution=contribution0, user=user2, value=1)

        new_rep = user1.relative_reputation() + user2.relative_reputation()
        # the rep is NOT LOWER
        self.assertGreater(new_rep, original_rep)
