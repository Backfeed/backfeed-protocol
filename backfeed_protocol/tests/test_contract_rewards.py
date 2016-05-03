from ..contracts.dmag import DMagContract
from ..models.evaluation import Evaluation

from test_contract_base import BaseContractTestCase


class TestContract(DMagContract):
    __mapper_args__ = {
        'polymorphic_identity': 'TestContract'
    }
    USER_INITIAL_TOKENS = 50.0
    USER_INITIAL_REPUTATION = 20.
    ALPHA = 0.7
    BETA = 0.5
    CONTRIBUTION_TYPE = {
        u'article': {
            'fee': 1,
            'distribution_stake': 0.08,
            'reputation_reward_factor': 5,
            'reward_threshold': 0.5,
            'stake': 0.02,
            'token_reward_factor': 50,
            'evaluation_set': [0, 1],
        },
        u'comment': {
            'fee': 0.1,
            'distribution_stake': 0.02,
            'reputation_reward_factor': 1,
            'reward_threshold': 0.5,
            'stake': 0.005,
            'token_reward_factor': 10,
            'evaluation_set': [0, 1],
        }
    }


class RewardsAndFeeTest(BaseContractTestCase):
    """test dmag protocol"""
    contract_class_to_test = TestContract
    contract_name = u'test'

    def setUp(self):
        super(RewardsAndFeeTest, self).setUp()
        self.contract = self.get_fresh_contract()
        self.allowedDeviation = 0.00005

    #
    # test evaluation rewards
    #
    def evaluation_reward(self, reputation_at_stake, new_reputation_at_stake, total_reputation=1.0):
        """return the reward for an evaluator that has put reputation_at_stake
        when a new evaluator adds an evaluation with the same value, putting
        new_reputation_at_stake
        """
        contract = self.get_fresh_contract()

        evaluator = contract.create_user(reputation=reputation_at_stake)
        new_evaluator = contract.create_user(reputation=new_reputation_at_stake)
        remaining_reputation = total_reputation - reputation_at_stake - new_reputation_at_stake
        contributor = contract.create_user(reputation=remaining_reputation)

        contribution = contract.create_contribution(user=contributor, contribution_type=u'article')
        contract.create_evaluation(user=evaluator, contribution=contribution, value=1)

        reputation_before_reward = evaluator.reputation

        contract.create_evaluation(user=new_evaluator, contribution=contribution, value=1)

        reward = evaluator.reputation - reputation_before_reward
        return reward

    def test_sum_equally_voted_reputation(self):
        contract = self.contract
        user0 = contract.create_user(reputation=10)
        user1 = contract.create_user(reputation=20)
        user2 = contract.create_user(reputation=3)
        contribution = contract.create_contribution(user=user0)
        contract.create_evaluation(contribution=contribution, user=user0, value=1)
        contract.create_evaluation(contribution=contribution, user=user1, value=0)
        evaluation = contract.create_evaluation(contribution=contribution, user=user2, value=1)

        self.assertEqual(contract.sum_equally_voted_reputation(evaluation), user0.reputation)

    def test_evaluation_reward(self):
        reward = self.evaluation_reward(reputation_at_stake=.2, new_reputation_at_stake=0.2)
        self.assertAlmostEqual(reward, 0.0042, places=4)

        # get a BIG confirmation of 80%
        reward = self.evaluation_reward(reputation_at_stake=.2, new_reputation_at_stake=0.8)
        self.assertAlmostEqual(reward, 0.0127, places=4)

        #
        reward = self.evaluation_reward(reputation_at_stake=.8, new_reputation_at_stake=0.2)
        self.assertAlmostEqual(reward, 0.0041, places=4)

        # a small stake with a small confirmation
        reward = self.evaluation_reward(reputation_at_stake=.01, new_reputation_at_stake=0.01)
        self.assertAlmostEqual(reward, 0.00002587, places=4)

    #
    # tests for rewarding the contributor
    #

    def contribution_reward(self, upvoted_reputation, total_reputation=1.0):
        """return

        upvoted_repution is the amount of repution in upvotes
        returns (token_reward, reputation_reward)
        """
        contract = self.get_fresh_contract()

        contributor = contract.create_user(reputation=0.0)
        evaluator = contract.create_user(reputation=upvoted_reputation)
        contract.create_user(reputation=total_reputation - upvoted_reputation)
        contribution = contract.create_contribution(user=contributor, contribution_type=u'article')
        contribution.user.tokens = 0
        evaluation = Evaluation(contract=contract, contribution=contribution, user=evaluator, value=1)
        contract.reward_contributor(evaluation)

        reputation_reward = evaluation.contribution.user.reputation
        token_reward = evaluation.contribution.user.tokens

        return (token_reward, reputation_reward)

    def test_contribution_reward(self):
        self.assertAlmostEqual(self.contribution_reward(0.0)[0], 0, places=4)
        self.assertAlmostEqual(self.contribution_reward(0.0)[1], 0, places=4)

        self.assertAlmostEqual(self.contribution_reward(0.8)[0], 40, places=4)
        self.assertAlmostEqual(self.contribution_reward(0.8)[1], 4, places=4)

        self.assertAlmostEqual(self.contribution_reward(1.0)[0], 50, places=4)
        self.assertAlmostEqual(self.contribution_reward(1.0)[1], 5, places=4)

        self.assertAlmostEqual(self.contribution_reward(0.6, 1)[1], 3, places=4)
        self.assertAlmostEqual(self.contribution_reward(30, 50)[1], 3, places=4)
        self.assertAlmostEqual(self.contribution_reward(33, 49)[1], 3.3673, places=4)

    def test_contribution_reward_increments(self):
        # test if the contributor does not get rewarded twice
        contract = self.contract
        contributor = contract.create_user(reputation=0, tokens=100)
        evaluator1 = contract.create_user(reputation=0.7)
        evaluator2 = contract.create_user(reputation=0)
        evaluator3 = contract.create_user(reputation=0)
        extra_user = contract.create_user(reputation=0.3)
        contribution = contract.create_contribution(user=contributor, contribution_type=u'article')
        contribution.user.tokens = 0

        # evaluator 1 upvotes the contribution with his 0.7 rep
        evaluation1 = contract.create_evaluation(contribution=contribution, user=evaluator1, value=1)
        # the contributor should recieve a reward as this point
        self.assertGreater(evaluation1.contribution.user.reputation, 0)
        self.assertGreater(evaluation1.contribution.user.tokens, 0)

        # now the situation changes
        # evaluator1 looses all its reputation, and we reset the contributor
        contributor.reputation = 0
        evaluator1.reputation = 0
        evaluator2.reputation = 0.6
        evaluator3.reputation = 0.2
        extra_user.reputation = 0.2
        contributor.reputation = 0
        contributor.tokens = 0

        contribution.evaluations[0].user = evaluator1
        contribution.user = contributor
        # sanity test
        self.assertEqual(contract.total_reputation(), 1.0)

        # evalualor2 now evaluates
        evaluation2 = contract.create_evaluation(contribution=contribution, user=evaluator2, value=1)

        # the contributor will not get new rewards, as the total upvotes
        # for this contribution have not reached the level of the previous payout
        self.assertEqual(evaluation2.contribution.user.tokens, 0)
        self.assertEqual(evaluation2.contribution.user.reputation, 0)

        # but if we add more rep, the contributor _will_ get rewarded
        evaluation3 = contract.create_evaluation(contribution=contribution, user=evaluator3, value=1)
        self.assertGreater(evaluation3.contribution.user.tokens, 0)
        self.assertGreater(evaluation3.contribution.user.reputation, 0)

    # Test Evaluation fee
    #
    def evaluation_fee(self, reputation_at_stake, total_reputation=1.0):
        """assert that the fee payed for evaluating a contribution is equal to reputation_fee

        reputation_at_stake: the reputation of the evaluator

        note that in the DMAG implementation, the evaluation fee depends
        exclusively on the (relative) repuation of the evaluator

        """
        contract = self.get_fresh_contract()
        contributor = contract.create_user(reputation=total_reputation - reputation_at_stake)
        evaluator = contract.create_user(reputation=reputation_at_stake)
        contribution = contract.create_contribution(user=contributor, contribution_type=u'article')
        # do not use contract.create_evaluation in the test, because that will call pay_evaluation_fee
        evaluation = Evaluation(user=evaluator, contribution=contribution, value=1, contract=contract)
        contract.pay_evaluation_fee(evaluation)
        fee_payed = reputation_at_stake - evaluation.user.reputation
        return fee_payed

    def test_evaluation_fee(self):
        self.assertAlmostEqual(self.evaluation_fee(reputation_at_stake=0.00), 0.0)
        self.assertAlmostEqual(self.evaluation_fee(reputation_at_stake=0.25), 0.0025, places=4)
        self.assertAlmostEqual(self.evaluation_fee(reputation_at_stake=0.33), 0.0028, places=4)
        self.assertAlmostEqual(self.evaluation_fee(reputation_at_stake=0.50), 0.0029, places=4)
        self.assertAlmostEqual(self.evaluation_fee(reputation_at_stake=1.00), 0.0000, places=4)

    def test_evaluation_fee_depends_only_on_relative_reputation(self):
        # make sure that the evaluation fee a user pays depends only on her repution as a fraction of the total
        fee1 = self.evaluation_fee(reputation_at_stake=0.314, total_reputation=1.0)
        fee2 = self.evaluation_fee(reputation_at_stake=314, total_reputation=1000)
        self.assertAlmostEqual(fee1 / 1.0, fee2 / 1000, places=4)
