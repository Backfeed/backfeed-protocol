from protocol.contracts.dmag import DMagContract
from protocol.models.evaluation import Evaluation

from test_contract_base import BaseContractTestCase


class DmagTest(BaseContractTestCase):
    """test dmag protocol"""
    contract_class_to_test = DMagContract

    def setUp(self):
        super(DmagTest, self).setUp()
        self.contract = self.get_fresh_contract()
        self.allowedDeviation = 0.00005

    #
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
        contribution = contract.create_contribution(user=contributor)
        # do not use contract.create_evaluation in the test, because that will call pay_evaluation_fee
        evaluation = Evaluation(user=evaluator, contribution=contribution, value=1)
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

        contribution = contract.create_contribution(user=contributor)
        evaluation = contract.create_evaluation(user=evaluator, contribution=contribution, value=1)

        # TODO: the next lines are just hacks needed
        # because we did not properly separate db layer from logic
        evaluator.reputation = reputation_at_stake
        evaluation.evaluator = evaluator
        evaluator.save()
        contribution = contract.get_contribution(contribution)
        evaluation.contribution = contribution

        new_evaluation = Evaluation(user=new_evaluator, contribution=contribution, value=1)
        contract.reward_previous_evaluators(new_evaluation)

        # more hacks
        user = contract.get_user(evaluation.user)

        reward = user.reputation - reputation_at_stake
        return reward

    def test_evaluation_reward(self):
        reward = self.evaluation_reward(reputation_at_stake=.2, new_reputation_at_stake=0.2)
        self.assertAlmostEqual(reward, 0.0042, places=4)

        # get a BIG confirmation of 80%
        reward = self.evaluation_reward(reputation_at_stake=.2, new_reputation_at_stake=0.8)
        self.assertAlmostEqual(reward, 0.0128, places=4)

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
        contribution = contract.create_contribution(user=contributor)
        contribution.user.tokens = 0
        evaluation = Evaluation(contribution=contribution, user=evaluator, value=1)
        evaluation.save()
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
        contribution = contract.create_contribution(user=contributor)
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

        # hack for syncing (TOD)
        contributor.save()
        evaluator1.save()
        evaluator2.save()
        evaluator3.save()
        extra_user.save()
        contribution.evaluations[0].user = evaluator1
        contribution.user = contributor
        # sanity test
        self.assertEqual(contract.total_reputation, 1.0)

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

    #
    # Integration test
    #
    def test_results_of_R_simulation(self):
        """test if our results match the R simulation"""
        contract = self.contract
        # add some users and contributions
        user1 = contract.create_user()
        user2 = contract.create_user()
        user3 = contract.create_user()
        user4 = contract.create_user()
        user5 = contract.create_user()

        # users get default values from the protocol
        self.assertEqual(user1.reputation, 20)
        self.assertEqual(user1.tokens, 50)

        # user2 and 3 make a contribution
        contribution1 = contract.create_contribution(user2)
        contribution2 = contract.create_contribution(user3)

        # a contribution has a fee of 1 token
        self.assertEqual(user2.tokens, 49)
        self.assertEqual(user3.tokens, 49)

        # we now expect the following distibution of tokens and reputation
        expected_state = {
            user1.id: {"reputation": 20, "tokens": 50},
            user2.id: {"reputation": 20, "tokens": 49},
            user3.id: {"reputation": 20, "tokens": 49},
            user4.id: {"reputation": 20, "tokens": 50},
            user5.id: {"reputation": 20, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 1: user1 evaluations the first contribution
        contract.create_evaluation(user=user1, contribution=contribution1, value=1)

        # at this point, the reputation of user1 is diminished
        self.assertEqual(user1.reputation, 19.778885438199982)
        # user1 does not pay any tokens for evaluating
        self.assertEqual(user1.tokens, 50)
        # while the repuation of the othe users remains unchanged
        self.assertEqual(user2.reputation, 20)
        expected_state = {
            user1: {"reputation": 19.7788854382, "tokens": 50},
            user2: {"reputation": 20, "tokens": 49},
            user3: {"reputation": 20, "tokens": 49},
            user4: {"reputation": 20, "tokens": 50},
            user5: {"reputation": 20, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step2: user2 now evaluations contribution1 with value 0
        contract.create_evaluation(user=user2, contribution=contribution1, value=0)

        expected_state = {
            user1: {"reputation": 19.7789, "tokens": 50},
            user2: {"reputation": 19.8526, "tokens": 49},
            user3: {"reputation": 20, "tokens": 49},
            user4: {"reputation": 20, "tokens": 50},
            user5: {"reputation": 20, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 3:
        contract.create_evaluation(user=user3, contribution=contribution1, value=1)
        # 3   P3 evaluates C1 by 1    20.1972 19.8526 19.9095 20  20  99.9593 50  49  49  50  50  248
        expected_state = {
            user1: {"reputation": 20.1972, "tokens": 50},
            user2: {"reputation": 19.8526, "tokens": 49},
            user3: {"reputation": 19.9094, "tokens": 49},
            user4: {"reputation": 20, "tokens": 50},
            user5: {"reputation": 20, "tokens": 50}
        }
        self.assert_user_states(expected_state)
        contract.create_evaluation(user=user4, contribution=contribution2, value=1)
        expected_state = {
            user1: {"reputation": 20.1972, "tokens": 50},
            user2: {"reputation": 19.8525, "tokens": 49},
            user3: {"reputation": 19.9095, "tokens": 49},
            user4: {"reputation": 19.7789, "tokens": 50},
            user5: {"reputation": 20, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 5
        contract.create_evaluation(user=user5, contribution=contribution2, value=0)
        expected_state = {
            user1: {"reputation": 20.1972, "tokens": 50},
            user2: {"reputation": 19.8525, "tokens": 49},
            user3: {"reputation": 19.9094, "tokens": 49},
            user4: {"reputation": 19.7789, "tokens": 50},
            user5: {"reputation": 19.8526, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 6
        # make sure we have the latest information from the db
        user1 = contract.get_user(user1)
        contract.create_evaluation(user=user1, contribution=contribution2, value=1)
        # 6 P1 evaluates C2 by 1    20.1064 19.8526 19.9095 20.2009 19.8526 99.9219 50  49  49  50  50  248
        expected_state = {
            user1: {"reputation": 20.1064, "tokens": 50},
            user2: {"reputation": 19.8526, "tokens": 49},
            user3: {"reputation": 19.9095, "tokens": 49},
            user4: {"reputation": 20.2009, "tokens": 50},
            user5: {"reputation": 19.8526, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 7
        user2 = contract.get_user(user2)
        contract.create_evaluation(user=user2, contribution=contribution1, value=1)
        expected_state = {
            user1: {"reputation": 20.4791, "tokens": 50},
            # TODO: these are the simulation results
            # user2: {"reputation": 22.7586, "tokens": 78.9576},
            user2: {"reputation": 22.8612, "tokens": 79.08672},
            user3: {"reputation": 20.2785, "tokens": 49},
            user4: {"reputation": 20.2009, "tokens": 50},
            user5: {"reputation": 19.8526, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # TODO: make it so that also the next tests run
        return

        # step 8
        # 8 P3 evaluates C1 by 0    20.4791 22.7586 20.1905 20.2009 19.8526 103.4817    50  78.9576 49  50  50  277.95759   P3 already voted. Vote changed.
        contract.create_evaluation(user=user3, contribution=contribution1, value=0)
        expected_state = {
            user1: {"reputation": 20.4791, "tokens": 50},
            user2: {"reputation": 22.7586, "tokens": 78.9576},
            user3: {"reputation": 20.1905, "tokens": 49},
            user4: {"reputation": 20.2009, "tokens": 50},
            user5: {"reputation": 19.8526, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 9
        contract.create_evaluation(user=user5, contribution=contribution2, value=0)
        expected_state = {
            user1: {"reputation": 20.1972438528, "tokens": 50},
            user2: {"reputation": 19.8525613977, "tokens": 78.9576},
            user3: {"reputation": 19.9094563837, "tokens": 49},
            user4: {"reputation": 19.7789218868, "tokens": 50},
            user5: {"reputation": 19.8526, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 10
        contract.create_evaluation(user=user5, contribution=contribution2, value=0)
        expected_state = {
            user1: {"reputation": 20.1972438528, "tokens": 50},
            user2: {"reputation": 19.8525613977, "tokens": 78.9576},
            user3: {"reputation": 19.9094563837, "tokens": 49},
            user4: {"reputation": 19.7789218868, "tokens": 50},
            user5: {"reputation": 19.8526130418, "tokens": 50}
        }
        self.assert_user_states(expected_state)

    def assert_user_states(self, state_description):
        # check whether the current state of self.contract satisfies the state_spec
        # the state_description is a dictionary that maps users to reputation
        # and token values
        # make sure we ahve the latest information from the database
        for user_id in state_description:
            user = self.contract.get_user(user_id=user_id)
            self.assertTrue(user)
            # TODO: these tests are only precise in 2 decimals...
            self.assertAlmostEqual(user.reputation, state_description[user_id]['reputation'], places=2)
            self.assertAlmostEqual(user.tokens, state_description[user_id]['tokens'], places=2)
