from peewee import *
from ..settings import database
from user import User
from contribution import Contribution


class Evaluation(Model):

    user = ForeignKeyField(User, related_name='evaluations')
    contribution = ForeignKeyField(Contribution, related_name='evaluations')
    value = FloatField()
    # TODO: add timestamp

    class Meta:
        database = database
