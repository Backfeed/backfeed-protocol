from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from ..models import Base


class Contribution(Base):
    __tablename__ = 'contribution'
    id = Column(Integer, primary_key=True)
    # the time that this object was added
    time = Column(DateTime, default=datetime.now())
    contribution_type = Column(Unicode(255))
    contract_id = Column(Integer, ForeignKey('contract.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    evaluations = relationship('Evaluation', backref='contribution')

    max_score = Column(Float)

    def engaged_reputation(self):
        """return the total amount of reputation of users that have voted for this contribution"""
        return sum([evaluation.user.reputation for evaluation in self.evaluations])

    def get_contract(self):
        from .. import utils
        return utils.get_contract(contract_id=self.contract.id)

    def get_statistics(self):
        """return information about evaluations, repuation engaged, etc"""
        evaluation_stats = {}
        possible_values = self.get_contract().CONTRIBUTION_TYPE[self.contribution_type]['evaluation_set']
        for value in possible_values:
            reputation = sum(evaluation.user.reputation for evaluation in self.contract.get_evaluations(value=value, contribution_id=self.id))
            if reputation:
                evaluation_stats[value] = {
                    'reputation': reputation,
                }

        return {
            'evaluations': evaluation_stats,
        }
