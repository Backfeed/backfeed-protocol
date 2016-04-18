from datetime import datetime
from peewee import Model, DateTimeField

from ..settings import database


class Contract(Model):
    # the time that this object was added
    time = DateTimeField(default=datetime.now())

    class Meta:
        database = database
        db_table = 'contract'

    def __init__(self):
        super(Contract, self).__init__()
        self._meta.db_table = 'contract'

    @property
    def total_reputation(self):
        """return the total reputation of all users in this contract"""
        return sum([user.reputation for user in self.users])
