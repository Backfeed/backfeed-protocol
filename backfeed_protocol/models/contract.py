from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy.orm import relationship

from ..models import Base


class Contract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True, autoincrement=True)

    # the name under which this contract was registered
    name = Column(Unicode(255), unique=True)
    # the time that this object was added
    time = Column(DateTime, default=datetime.now())
    users = relationship('User', backref='contract')
    evaluations = relationship('Evaluation', backref='contract')
    contributions = relationship('Contribution', backref='contract')

    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def relative_reputation(self):
        """return the reputation as a fraction of the total reputation"""
        return self.reputation / self.contract.total_reputation
