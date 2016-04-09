from peewee import *

from ..settings import database


class User(Model):
    reputation = FloatField()
    tokens = FloatField()

    class Meta:
        database = database
