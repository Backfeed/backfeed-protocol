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
