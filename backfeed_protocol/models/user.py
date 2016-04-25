
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from ..models import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True)
    contract_id = Column(Integer, ForeignKey('contract.id'))
    reputation = Column(Float)
    tokens = Column(Float)
    # the time that this object was added
    time = Column(DateTime, default=datetime.now())
    evaluations = relationship('Evaluation', backref='user')
    contributions = relationship('Contribution', backref='user')

    referrer_id = Column(Integer, ForeignKey('user.id'))
    referrer = relationship('User', remote_side=[id])

    def relative_reputation(self):
        """return the reputation as a fraction of the total reputation"""
        return self.reputation / self.contract.total_reputation()
