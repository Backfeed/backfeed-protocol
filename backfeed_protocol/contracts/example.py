from base import BaseContract


class ExampleContract(BaseContract):
    __mapper_args__ = {
        'polymorphic_identity': 'ExampleContract'
    }
    USER_INITIAL_TOKENS = 50.0
    USER_INITIAL_REPUTATION = 20
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
            'token_fund_for_evaluators': 10
        },
        u'comment': {
            'fee': 0.1,
            'distribution_stake': 0.02,
            'reputation_reward_factor': 1,
            'reward_threshold': 0.5,
            'stake': 0.005,
            'token_reward_factor': 10,
            'evaluation_set': [0, 1],
            'token_fund_for_evaluators': 2
        }
    }
