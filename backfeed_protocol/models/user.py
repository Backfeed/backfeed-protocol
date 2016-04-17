from datetime import datetime
from peewee import FloatField, Model, DateTimeField


from ..settings import database


class User(Model):
    reputation = FloatField()
    tokens = FloatField()
    # the time that this object was added
    time = DateTimeField(default=datetime.now())

    class Meta:
        database = database
