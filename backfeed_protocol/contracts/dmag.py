from base import BaseContract


class DMagContract(BaseContract):
    __mapper_args__ = {
        'polymorphic_identity': 'DmagContract'
    }
    USER_INITIAL_TOKENS = 50.0
    USER_INITIAL_REPUTATION = 0
    BETA = 0.6
    REWARD_TOKENS_TO_EVALUATORS = True
    CONTRIBUTION_TYPE = {
        u'article': {
            'fee': 1,
            'distribution_stake': 0.06,
            'reputation_reward_factor': 50,
            'reward_threshold': 0.3,
            'stake': 0.02,
            'token_reward_factor': 20,
            'evaluation_set': [0, 1],
            'token_fund_for_evaluators': 10
        },
        u'comment': {
            'fee': 0.2,
            'distribution_stake': 0.01,
            'reputation_reward_factor': 5,
            'reward_threshold': 0.2,
            'stake': 0.003,
            'token_reward_factor': 5,
            'evaluation_set': [0, 1],
            'token_fund_for_evaluators': 2
        }
    }
