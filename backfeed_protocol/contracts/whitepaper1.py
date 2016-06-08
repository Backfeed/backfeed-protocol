"""
this contract implements the flow function of the first example in the whitepaper
"""

from base import BaseContract


class WhitePaper1Contract(BaseContract):
    __mapper_args__ = {
        'polymorphic_identity': 'WhitePaper1Contract'
    }
    USER_INITIAL_TOKENS = 50.0
    USER_INITIAL_REPUTATION = 20

    CONTRIBUTION_TYPE = {
        u'contribution': {
            'fee': 1,
            'reputation_reward_factor': .02,
            'evaluation_set': [True, False],
        },
    }

    def reward_evaluators(self, evaluation, previously_voted=False):

        engaged_equal_rep = evaluation.contribution.engaged_reputation(value=evaluation.value)
        engaged_unequal_rep = sum([
            evaluation.contribution.engaged_reputation(value=value)
            for value in self.CONTRIBUTION_TYPE['contribution']['evaluation_set']
            if value != evaluation.value
        ])
        unengaged_rep = self.total_reputation() - engaged_equal_rep - engaged_unequal_rep
        rep_to_be_distributed = (
            evaluation.user.reputation *
            self.CONTRIBUTION_TYPE['contribution']['reputation_reward_factor'] *
            unengaged_rep
        )

        if not engaged_equal_rep - evaluation.user.reputation:
            # there is no 'benefactor to be distributed to'
            return evaluation
        if not rep_to_be_distributed:
            # there is nothing to be distributed
            return evaluation
        # TODO: this is highly ineffecient
        for user in self.users:
            evaluations = self.get_evaluations(evaluator_id=user.id, contribution_id=evaluation.contribution.id)
            user_evaluation = evaluations and evaluations[0] or None
            if user == evaluation.user:
                # the evaluator gets nothing
                pass
            elif user_evaluation and user_evaluation.value == evaluation.value:
                # reward previous equal voters
                user.reputation += (user.reputation / (engaged_equal_rep - evaluation.user.reputation)) * rep_to_be_distributed
            elif user_evaluation and user_evaluation.value != evaluation.value:
                pass
            else:
                # we have a non-voter
                user.reputation -= (user.reputation / unengaged_rep) * rep_to_be_distributed

        return evaluation
