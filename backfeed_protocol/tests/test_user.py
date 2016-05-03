from datetime import datetime
from ..contracts.dmag import DMagContract

from test_contract_base import BaseContractTestCase


class UserTest(BaseContractTestCase):
    """test dmag protocol"""
    contract_class_to_test = DMagContract
    contract_name = 'dmag'

    def test_get_user(self):
        user_id = self.contract.create_user().id
        user = self.contract.get_user(user_id=user_id)

        self.assertEqual(user.id, user_id)
        self.assertTrue(isinstance(user.time, datetime))

    def test_user_referral(self):
        contract = self.contract
        referrer1 = contract.create_user(reputation=100, tokens=100)
        referrer2 = contract.create_user(reputation=100, tokens=100)
        contributor = contract.create_user(referrer=referrer1, reputation=100, tokens=100)
        evaluator1 = contract.create_user(reputation=1000, tokens=1000, referrer=referrer2)
        evaluator2 = contract.create_user(reputation=1000, tokens=1000)

        self.assertEqual(contributor.referrer, referrer1)

        # if we reward contributor, then referrer1 should get a part of the rewards

        contribution = contract.create_contribution(user=contributor)

        contributor_tokens_pre = contributor.tokens
        contributor_reputation_pre = contributor.reputation

        contract.create_evaluation(contribution=contribution, user=evaluator1, value=1)

        evaluator1_reputation_pre = evaluator1.reputation

        contract.create_evaluation(contribution=contribution, user=evaluator2, value=1)

        # contributor is now rewarded for the contribution
        contributor_reputation_delta = contributor.reputation - contributor_reputation_pre
        contributor_tokens_delta = contributor.tokens - contributor_tokens_pre
        self.assertGreater(contributor_reputation_delta, 0)
        self.assertGreater(contributor_tokens_delta, 0)

        # and also the referrer of contributor, which is referrer1, should be rewarded
        self.assertLess(100, referrer1.reputation)
        self.assertLess(100, referrer1.tokens)

        # to be precise, the reward for referrer1 is REFERRAL_REWARD_FRACTION * contributor's reward
        self.assertAlmostEqual(contributor_reputation_delta * contract.REFERRAL_REWARD_FRACTION, (referrer1.reputation - 100),)

        # We also get a similar thing going on for referrer the evaluator1
        evaluator1_reputation_delta = evaluator1.reputation - evaluator1_reputation_pre
        self.assertGreater(evaluator1_reputation_delta, 0)
        self.assertGreater(referrer2.reputation, 100)

        self.assertAlmostEqual(evaluator1_reputation_delta * contract.REFERRAL_REWARD_FRACTION, (referrer2.reputation - 100),)
