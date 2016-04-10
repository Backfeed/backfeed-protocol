from peewee import ForeignKeyField, FloatField, Model
from user import User
from ..settings import database


class Contribution(Model):
    # the user that has made the contribution
    user = ForeignKeyField(User, related_name='contributions')
    # max_score: it a a memo field
    max_score = FloatField(default=0)

    # TODO: add timestamp

    class Meta:
        database = database

    @property
    def committed_reputation(self):
        """return the total amount of reputation of users that have voted for this contribution"""
        return sum([evaluation.user.reputation for evaluation in self.evaluations])
