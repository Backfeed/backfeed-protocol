from datetime import datetime
from ..models import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime


class Evaluation(Base):
    __tablename__ = 'evaluation'
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contract.id'), nullable=False)
    contribution_id = Column(Integer, ForeignKey('contribution.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # the time that this object was added
    time = Column(DateTime, default=datetime.now())
    value = Column(Float)
