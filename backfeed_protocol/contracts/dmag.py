from base import BaseContract


class DMagContract(BaseContract):
    USER_INITIAL_TOKENS = 50.0
    USER_INITIAL_REPUTATION = 20.
    ALPHA = 0.7
    BETA = 0.5
    CONTRIBUTION_TYPE = {
        'article': {
            'fee': 1,
            'distribution_stake': 0.08,
            'reputation_reward_factor': 5,
            'reward_threshold': 0.5,
            'stake': 0.02,
            'token_reward_factor': 50,
            'evaluation_set': [0, 1],
        },
        'comment': {
            'fee': 0.1,
            'distribution_stake': 0.02,
            'reputation_reward_factor': 1,
            'reward_threshold': 0.5,
            'stake': 0.005,
            'token_reward_factor': 10,
            'evaluation_set': [0, 1],
        }
    }
