from datetime import datetime
from peewee import ForeignKeyField, FloatField, Model, DateTimeField, CharField
from user import User
from contract import Contract
from ..settings import database


class Contribution(Model):
    # the user that has made the contribution
    contract = ForeignKeyField(Contract, related_name='contributions')
    user = ForeignKeyField(User, related_name='contributions')
    # max_score: it a a memo field
    max_score = FloatField(default=0)

    # the time that this object was added
    time = DateTimeField(default=datetime.now())

    # contribution type
    contribution_type = CharField()

    class Meta:
        database = database

    def engaged_reputation(self):
        """return the total amount of reputation of users that have voted for this contribution"""
        return sum([evaluation.user.reputation for evaluation in self.evaluations])

    def get_statistics(self):
        """return information about evaluations, repuation engaged, etc"""
        evaluation_stats = {}

        possible_values = self.contract.CONTRIBUTION_TYPE[self.contribution_type]['evaluation_set']
        for value in possible_values:
            reputation = sum(evaluation.user.reputation for evaluation in self.evaluations.filter(value=value))
            if reputation:
                evaluation_stats[value] = {
                    'reputation':  reputation
                }

        return {
            'evaluations': evaluation_stats,
        }
