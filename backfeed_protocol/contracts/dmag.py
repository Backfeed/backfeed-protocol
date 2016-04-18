from base import BaseContract


class DMagContract(BaseContract):
    ALPHA = 0.7
    BETA = 0.5
    CONTRIBUTION_FEE = 1
    DISTRIBUTION_STAKE = 0.08  # stake distribution factor
    GAMMA = 0.5
    REPUTATION_REWARD_FACTOR = 5
    REWARD_THRESHOLD = 0.5  # rewardScoreThreshold
    STAKE = 0.02  # reputation stake multiplier
    TOKEN_REWARD_FACTOR = 50
    USER_INITIAL_TOKENS = 50.0
    USER_INITIAL_REPUTATION = 20.0
