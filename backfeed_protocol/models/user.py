from datetime import datetime
from peewee import FloatField, Model, DateTimeField, ForeignKeyField


from ..settings import database
from contract import Contract


class User(Model):
    contract = ForeignKeyField(Contract, related_name='users')
    reputation = FloatField()
    tokens = FloatField()
    # the time that this object was added
    time = DateTimeField(default=datetime.now())

    class Meta:
        database = database

    def relative_reputation(self):
        """return the reputation as a fraction of the total reputation"""
        return self.reputation / self.contract.total_reputation
