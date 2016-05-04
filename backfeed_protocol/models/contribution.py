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
    contract_id = Column(Integer, ForeignKey('contract.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    evaluations = relationship('Evaluation', backref='contribution')

    max_score = Column(Float)

    token_fund = Column(Float)

    def engaged_reputation(self):
        """return the total amount of reputation of users that have voted for this contribution"""
        return sum([evaluation.user.reputation for evaluation in self.contract.get_evaluations(contribution_id=self.id)])

    def engaged_reputation_normal(self):
        engaged_reputation = self.engaged_reputation()
        if engaged_reputation:
            engaged_reputation_normal = engaged_reputation / self.contract.total_reputation()
            return engaged_reputation_normal
        else:
            return 0

    def get_voted_rep_by_value(self, value):
        voted_rep = sum(evaluation.user.reputation for evaluation in self.contract.get_evaluations(value=value, contribution_id=self.id))
        return voted_rep

    def get_statistics(self):
        """return information about evaluations, repuation engaged, etc"""
        evaluation_stats = {}
        total_reputation = self.contract.total_reputation()
        engaged_reputation = self.engaged_reputation()
        possible_values = self.contract.CONTRIBUTION_TYPE[self.contribution_type]['evaluation_set']
        for value in possible_values:
            reputation = sum(evaluation.user.reputation for evaluation in self.contract.get_evaluations(value=value, contribution_id=self.id))
            if total_reputation:
                reputation_normal = reputation / total_reputation
            else:
                reputation_normal = 0
            evaluation_stats[value] = {
                'reputation': reputation,
                'reputation_normal': reputation_normal,
            }

        if total_reputation:
            engaged_reputation_normal = engaged_reputation / total_reputation
        else:
            engaged_reputation_normal = 0

        return {
            'evaluations': evaluation_stats,
            'score': self.contract.contribution_score(self),
            'engaged_reputation': engaged_reputation,
            'engaged_reputation_normal': engaged_reputation_normal,
        }
