from __future__ import division  # do division with floating point arithmetic

from ..models.user import User
from ..models.contribution import Contribution
from ..models.evaluation import Evaluation


class BaseContract(object):
    """The BaseContract class defines functions common to all protocols.
    """
    ALPHA = 0.7
    BETA = 0.5
    CONTRIBUTION_FEE = 1
    DURATION = 86400000
    DISTRIBUTION_STAKE = 0.08  # stake distribution factor
    GAMMA = 0.5
    REPUTATION_REWARD_FACTOR = 5
    REWARD_THRESHOLD = 0.5  # rewardScoreThreshold
    STAKE = 0.02  # reputation stake multiplier
    TOKEN_REWARD_FACTOR = 50
    USER_INITIAL_TOKENS = 50.0
    USER_INITIAL_REPUTATION = 20.0

    def __init__(self):
        pass

    def add_user(self, tokens=None, reputation=None):
        """create a new user with default values"""
        if tokens is None:
            tokens = self.USER_INITIAL_TOKENS
        if reputation is None:
            reputation = self.USER_INITIAL_REPUTATION
        new_user = User(contract=self, reputation=reputation, tokens=tokens)
        new_user.save()
        return new_user

    def get_users(self):
        return User.select()

    def get_user(self, user_id):
        return User.get(id=user_id)

    def delete_users(self):
        User.delete().execute()

    def add_contribution(self, user):
        # the user pays the fee for the contribution
        if user.tokens < self.CONTRIBUTION_FEE:
            msg = 'User does not have enough tokens to pay the contribution fee.'
            raise Exception(msg)
        user.tokens = user.tokens - self.CONTRIBUTION_FEE
        new_contribution = Contribution(user=user)
        new_contribution.save()
        user.save()
        return new_contribution

    def get_contribution(self, contribution_id):
        return Contribution.get(id=contribution_id)

    def get_contributions(self):
        return Contribution.select()

    def add_evaluation(self, user, contribution, value):
        evaluation = Evaluation(user=user, contribution=contribution, value=value)

        # disactivate any previous evaluations by this user
        for previous_evaluation in evaluation.contribution.evaluations.filter(user=user):
            # TODO: we should not remove the evaluation from the database
            # because it will interest us for auditing
            previous_evaluation.delete_instance()

        #  have the user has to pay his fees to make the evaluation
        self.pay_evaluation_fee(evaluation)

        # update users reputation for previous, equally voting users
        self.reward_previous_evaluators(evaluation)
        evaluation.save()

        self.reward_contributor(evaluation)
        evaluation.save()

        return evaluation

    def pay_evaluation_fee(self, evaluation):
        """calculate the fee for the evaluator of this evaluation

        returns a pair (token_fee, repution_fee)
         """
        user = evaluation.user
        contribution = evaluation.contribution

        # currentVotersLogical <- previousVotersLogical | (1:length(users$reputation) == evaluatorInd) ; # logical indexing of voters including current evaluator
        #  votedRep <- sum(users$reputation[currentVotersLogical]) ;
        votedRep = user.reputation + contribution.committed_reputation
        # 'stakeFee'
        #   x <- 1 - (votedRep/totalRep)^beta ;
        #  return(currentEvaluatorRep * x);
        stakeFee = user.reputation * (1 - ((votedRep / self.total_reputation) ** self.BETA))

        fee = self.STAKE * stakeFee
        evaluation.user.reputation -= fee
        evaluation.user.save()

    def reward_previous_evaluators(self, evaluation):
        """award the evaluators of this contribution that have previously voted evaluation.value"""
        contribution = evaluation.contribution
        # find previous evaluations with the same value
        equallyVotedRep = self.sum_equally_voted_reputation(evaluation)
        if equallyVotedRep:
            # add the rep of the current user, because that is what the R code seems to do
            equallyVotedRep += evaluation.user.reputation
            stake_distribution = evaluation.user.reputation / equallyVotedRep
            burn_factor = (equallyVotedRep / self.total_reputation) ** self.ALPHA
            # update previous voters
            for e in contribution.evaluations:
                if e.value == evaluation.value:
                    e.user.reputation *= 1 + \
                        (self.DISTRIBUTION_STAKE * stake_distribution * burn_factor)
                    e.user.save()

    def sum_equally_voted_reputation(self, evaluation):
        """return the sum of reputation of evaluators of evaluation.contribution that
        have evaluated the same value"""
        contribution = evaluation.contribution
        equallyVotedRep = sum(e.user.reputation for e in contribution.evaluations.filter(value=evaluation.value))
        return equallyVotedRep

    def reward_contributor(self, evaluation):
        # don't reward anything if the value is 0/
        if evaluation.value == 0:
            return
        contribution = evaluation.contribution
        contributor = evaluation.contribution.user
        rewardBase = 0
        upVotedRep = sum(e.user.reputation for e in contribution.evaluations if e.value == 1)

        currentScore = upVotedRep / self.total_reputation

        # TODO:
        # I think to keep track of 'already payed out rewards'
        # but probably it is better in that case to just count 'the difference'
        # of the current evaluation

        max_score = evaluation.contribution.max_score
        if currentScore > max_score:
            if max_score >= self.REWARD_THRESHOLD:
                rewardBase = currentScore - max_score
            elif currentScore > self.REWARD_THRESHOLD:
                rewardBase = currentScore
            contribution.max_score = currentScore
            contribution.save()
        if rewardBase > 0:
            # calc token reward by score/score_delta * tokenRewardFactor
            tokenReward = self.TOKEN_REWARD_FACTOR * rewardBase
            # calc token reward by score/score_delta * reputationRewardFactor
            reputationReward = self.REPUTATION_REWARD_FACTOR * rewardBase
            contributor.tokens = contributor.tokens + tokenReward
            contributor.reputation = contributor.reputation + reputationReward
            contributor.save()

    def get_evaluations(self):
        return Evaluation.select()

    @property
    def total_reputation(self):
        """return the total reputation of all users in this contract"""
        return sum([user.reputation for user in self.get_users()])
