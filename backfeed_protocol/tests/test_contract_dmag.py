from ..contracts.dmag import DMagContract

from test_contract_base import BaseContractTestCase


class DmagTest(BaseContractTestCase):
    """test dmag protocol"""
    contract_class_to_test = DMagContract
    contract_name = u'dmag'

    def setUp(self):
        super(DmagTest, self).setUp()
        self.contract = self.get_fresh_contract()
        self.allowedDeviation = 0.00005

    # Test contribution types
    def test_contribution_types(self,):
        contract = self.get_fresh_contract()
        contributor1 = contract.create_user()
        contributor2 = contract.create_user()
        contract.create_contribution(user=contributor1, contribution_type=u'article')
        contract.create_contribution(user=contributor2, contribution_type=u'comment')
        self.assertEqual(contributor1.tokens, contract.USER_INITIAL_TOKENS - contract.CONTRIBUTION_TYPE['article']['fee'])
        self.assertEqual(contributor2.tokens, contract.USER_INITIAL_TOKENS - contract.CONTRIBUTION_TYPE['comment']['fee'])
        self.assertRaises(KeyError, contract.create_contribution, contributor1, contribution_type='spam')

    #
    # Integration test
    #
    def test_results_of_R_simulation(self):
        """test if our results match the R simulation"""
        contract = self.contract
        contract.REWARD_TOKENS_TO_EVALUATORS = False
        contract.USER_INITIAL_TOKENS = 50.0
        contract.USER_INITIAL_REPUTATION = 20
        contract.ALPHA = 0.7
        contract.BETA = 0.5
        contract.CONTRIBUTION_TYPE = {
            u'article': {
                'fee': 1,
                'distribution_stake': 0.08,
                'reputation_reward_factor': 5,
                'reward_threshold': 0.5,
                'stake': 0.02,
                'token_reward_factor': 50,
                'evaluation_set': [0, 1],
                'token_fund_for_evaluators': 1
            },
            u'comment': {
                'fee': 0.1,
                'distribution_stake': 0.02,
                'reputation_reward_factor': 1,
                'reward_threshold': 0.5,
                'stake': 0.005,
                'token_reward_factor': 10,
                'evaluation_set': [0, 1],
                'token_fund_for_evaluators': 1
            }
        }
        # add some users and contributions
        user1 = contract.create_user(50, 20)
        user2 = contract.create_user(50, 20)
        user3 = contract.create_user(50, 20)
        user4 = contract.create_user(50, 20)
        user5 = contract.create_user(50, 20)

        # users get default values from the protocol
        self.assertEqual(user1.reputation, 20)
        self.assertEqual(user1.tokens, 50)

        # user2 and 3 make a contribution
        contribution1 = contract.create_contribution(user2, contribution_type=u'article')
        contribution2 = contract.create_contribution(user3, contribution_type=u'article')

        # a contribution has a fee of 1 token
        self.assertEqual(user2.tokens, 50 - contract.CONTRIBUTION_TYPE['article']['fee'])
        self.assertEqual(user3.tokens, 50 - contract.CONTRIBUTION_TYPE['article']['fee'])

        # we now expect the following distibution of tokens and reputation
        expected_state = {
            user1: {"reputation": 20, "tokens": 50},
            user2: {"reputation": 20, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user3: {"reputation": 20, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user4: {"reputation": 20, "tokens": 50},
            user5: {"reputation": 20, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        """20   20  20  20  20  50  49  49  50  50
        19.7788854382   20  20  20  20  50  49  49  50  50
        19.7788854382   19.8525613977   20  20  20  50  49  49  50  50
        20.5744385653   19.8525613977   19.9094563837   20  20  50  49  49  50  50
        20.5744385653   19.8525613977   19.9094563837   19.7785852598   20  50  49  49  50  50
        20.5744385653   19.8525613977   19.9094563837   19.7785852598   19.8521360773   50  49  49  50  50
        20.4822845066   19.8525613977   19.9094563837   20.5853318156   19.8521360773   50  49  49  50  50
        21.0222536593   22.7544628224   20.4343242172   20.5853318156   19.8521360773   50  78.9181779282   49  50  50
        21.0222536593   22.7544628224   20.3457693792   20.5853318156   19.8521360773   50  78.9181779282   49  50  50
        21.5601483702   23.4226197071   20.3457693792   20.5441923339   19.8521360773   50  79.7775807021   49  50  50
        22.1128137528   23.4226197071   23.2758500312   21.070815051    19.7590362707   50  79.7775807021   78.3008065193   50  50
        """

        # step 1: user1 evaluations the first contribution
        contract.create_evaluation(user=user1, contribution=contribution1, value=1)

        # at this point, the reputation of user1 is diminished
        self.assertEqual(user1.reputation, 19.778885438199982)
        # user1 does not pay any tokens for evaluating
        self.assertEqual(user1.tokens, 50)
        # while the repuation of the othe users remains unchanged
        self.assertEqual(user2.reputation, 20)

        expected_state = {
            user1: {"reputation": 19.778885, "tokens": 50},
            user2: {"reputation": 20, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user3: {"reputation": 20, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user4: {"reputation": 20, "tokens": 50},
            user5: {"reputation": 20, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step2: user2 now evaluations contribution1 with value 0
        contract.create_evaluation(user=user2, contribution=contribution1, value=0)

        expected_state = {
            user1: {"reputation": 19.778885, "tokens": 50},
            user2: {"reputation": 19.852561, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user3: {"reputation": 20, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user4: {"reputation": 20, "tokens": 50},
            user5: {"reputation": 20, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 3:
        contract.create_evaluation(user=user3, contribution=contribution1, value=1)
        expected_state = {
            user1: {"reputation": 20.5744385, "tokens": 50},
            user2: {"reputation": 19.8525613, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user3: {"reputation": 19.9094563, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user4: {"reputation": 20, "tokens": 50},
            user5: {"reputation": 20, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 4
        contract.create_evaluation(user=user4, contribution=contribution2, value=1)
        expected_state = {
            user1: {"reputation": 20.5744385, "tokens": 50},
            user2: {"reputation": 19.8525613, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user3: {"reputation": 19.9094563, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user4: {"reputation": 19.7785852, "tokens": 50},
            user5: {"reputation": 20, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 5
        contract.create_evaluation(user=user5, contribution=contribution2, value=0)
        expected_state = {
            user1: {"reputation": 20.5744385, "tokens": 50},
            user2: {"reputation": 19.8525613, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user3: {"reputation": 19.9094563, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user4: {"reputation": 19.7785852, "tokens": 50},
            user5: {"reputation": 19.8521360, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 6
        contract.create_evaluation(user=user1, contribution=contribution2, value=1)
        expected_state = {
            user1: {"reputation": 20.4822845, "tokens": 50},
            user2: {"reputation": 19.8525613, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user3: {"reputation": 19.9094563, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user4: {"reputation": 20.5853318, "tokens": 50},
            user5: {"reputation": 19.8521360, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 7
        contract.create_evaluation(user=user2, contribution=contribution1, value=1)
        expected_state = {
            user1: {"reputation": 21.0222536, "tokens": 50},
            user2: {"reputation": 22.7544628, "tokens": 78.9181779},
            user3: {"reputation": 20.4343242, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user4: {"reputation": 20.5853318, "tokens": 50},
            user5: {"reputation": 19.8521360, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 8

        contract.create_evaluation(user=user3, contribution=contribution1, value=0)
        expected_state = {
            user1: {"reputation": 21.0222536, "tokens": 50},
            user2: {"reputation": 22.7544628, "tokens": 78.9181779},
            user3: {"reputation": 20.3457693, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user4: {"reputation": 20.5853318, "tokens": 50},
            user5: {"reputation": 19.8521360, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 9

        contract.create_evaluation(user=user4, contribution=contribution1, value=1)
        expected_state = {
            user1: {"reputation": 21.5601483, "tokens": 50},
            user2: {"reputation": 23.4226197, "tokens": 79.7775807},
            user3: {"reputation": 20.3457693, "tokens": 50 - contract.CONTRIBUTION_TYPE['article']['fee']},
            user4: {"reputation": 20.5441923, "tokens": 50},
            user5: {"reputation": 19.8521360, "tokens": 50}
        }
        self.assert_user_states(expected_state)

        # step 10
        # 22.1128137528 23.4226197071   23.2758500312   21.070815051    19.7590362707   50  79.7775807021   78.3008065193

        contract.create_evaluation(user=user5, contribution=contribution2, value=1)
        expected_state = {
            user1: {"reputation": 22.1128137, "tokens": 50},
            user2: {"reputation": 23.4226197, "tokens": 79.7775807},
            user3: {"reputation": 23.2758500, "tokens": 78.3008065},
            user4: {"reputation": 21.070815, "tokens": 50},
            user5: {"reputation": 19.7590362, "tokens": 50}
        }
        self.assert_user_states(expected_state)

    def assert_user_states(self, state_description):
        # check whether the current state of self.contract satisfies the state_description given
        # the state_description is a dictionary that maps users to reputation
        # and token values
        for user in state_description:
            user = self.contract.get_user(user_id=user.id)
            # self.assertTrue(user)
            # TODO: these tests are only precise in 2 decimals...
            self.assertAlmostEqual(user.reputation, state_description[user]['reputation'], places=3)
            self.assertAlmostEqual(user.tokens, state_description[user]['tokens'], places=2)
