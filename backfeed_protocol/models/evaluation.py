from datetime import datetime
from peewee import ForeignKeyField, FloatField, Model, DateTimeField

from ..settings import database
from user import User
from contribution import Contribution


class Evaluation(Model):

    user = ForeignKeyField(User, related_name='evaluations')
    contribution = ForeignKeyField(Contribution, related_name='evaluations')
    value = FloatField()
    # the time that this object was added
    time = DateTimeField(default=datetime.now())

    class Meta:
        database = database
