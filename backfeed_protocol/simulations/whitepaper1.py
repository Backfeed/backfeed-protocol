import random
from ..contracts.whitepaper1 import WhitePaper1Contract
from simulation import Simulation, StepEvaluate


class WhitePaper1(Simulation):
    """Simulation of Whitepaper Protocol in which 4 users consecutively value the contribution as True"""
    name = 'whitepaper1'
    contract_class_to_test = WhitePaper1Contract

    def init(self):
        self.contributor = self.contract.create_user()
        self.evaluator1 = self.contract.create_user()
        self.evaluator2 = self.contract.create_user()
        self.evaluator3 = self.contract.create_user()
        self.contribution = self.contract.create_contribution(user=self.contributor)

    @property
    def steps(self):
        contribution = self.contribution
        steps = [
            StepEvaluate(user=self.contributor, contribution=contribution, value=True),
            StepEvaluate(user=self.evaluator1, contribution=contribution, value=True),
            StepEvaluate(user=self.evaluator2, contribution=contribution, value=True),
            StepEvaluate(user=self.evaluator3, contribution=contribution, value=True),
        ]
        return steps


class WhitePaper2(WhitePaper1):
    """Simulation of Whitepaper Protocol in which 4 users vote - two positive, two negative"""
    name = 'whitepaper2'

    @property
    def steps(self):
        contribution = self.contribution
        steps = [
            StepEvaluate(user=self.contributor, contribution=contribution, value=True),
            StepEvaluate(user=self.evaluator1, contribution=contribution, value=False),
            StepEvaluate(user=self.evaluator2, contribution=contribution, value=True),
            StepEvaluate(user=self.evaluator3, contribution=contribution, value=False),
        ]
        return steps


class WhitePaper3(WhitePaper1):
    """Whitepaper Protocol in which 20 users vote - all equal"""
    name = 'whitepaper3'

    def init(self):
        self.contributor = self.contract.create_user()
        self.contribution = self.contract.create_contribution(user=self.contributor)
        self.evaluators = []
        for i in range(0, 19):
            self.evaluators.append(self.contract.create_user())

    @property
    def steps(self):
        contribution = self.contribution
        steps = [StepEvaluate(user=self.contributor, contribution=contribution, value=True)]
        for evaluator in self.evaluators:
            steps.append(
                StepEvaluate(user=evaluator, contribution=contribution, value=True),
            )
        return steps


class WhitePaper4(WhitePaper1):
    """Whitepaper Protocol in which 100 users vote - all equal"""
    name = 'whitepaper4'

    def init(self):
        self.contributor = self.contract.create_user()
        self.contribution = self.contract.create_contribution(user=self.contributor)
        self.evaluators = []
        for i in range(0, 100):
            self.evaluators.append(self.contract.create_user())

    @property
    def steps(self):
        contribution = self.contribution
        steps = [StepEvaluate(user=self.contributor, contribution=contribution, value=True)]
        for evaluator in self.evaluators:
            steps.append(
                StepEvaluate(user=evaluator, contribution=contribution, value=True),
            )
        return steps


class WhitePaper5(WhitePaper1):
    """Whitepaper Protocol in which 100 users vote randomly, with 75% yes"""
    name = 'whitepaper5'

    def init(self):
        self.contributor = self.contract.create_user()
        self.contribution = self.contract.create_contribution(user=self.contributor)
        self.evaluators = []
        for i in range(0, 100):
            self.evaluators.append(self.contract.create_user())

    @property
    def steps(self):
        contribution = self.contribution
        steps = [StepEvaluate(user=self.contributor, contribution=contribution, value=True)]
        for evaluator in self.evaluators:
            value = random.choice([True, True, True, False])
            steps.append(
                StepEvaluate(user=evaluator, contribution=contribution, value=value),
            )
        return steps
