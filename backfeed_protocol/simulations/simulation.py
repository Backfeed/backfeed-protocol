from ..models import with_session
from ..models import DBSession
from backfeed_protocol import utils


class Step(object):
    pass


class StepEvaluate(Step):
    def __init__(self, user, contribution, value, description=None):
        self.user = user
        self.contribution = contribution
        self.value = value
        self.description = description

    def __unicode__(self):
        if self.description:
            msg = self.description + '\n'
        else:
            msg = ''

        msg += 'create_evaluation (user={self.user.id}, contribution={self.contribution.id}, value={self.value})'.format(self=self)
        return msg

    def execute(self, contract):
        contract.create_evaluation(user=self.user, contribution=self.contribution, value=self.value)


class Simulation(object):
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:',
    }
    contract_name = u'sim'

    def __init__(self):
        utils.setup_database(settings=self.settings)
        self.contract = self.get_fresh_contract()

    @with_session
    def get_fresh_contract(self):
        """get a contract with default settings but without users or other data"""
        utils.reset_database()
        contract = self.contract_class_to_test(name=self.contract_name)
        DBSession.add(contract)
        return contract

    # Test contribution types
    def run(self):
        print('')
        print('')
        print('')
        print('-' * 100)
        print(self.__doc__)
        print('-' * 100)
        self.init()
        for i, step in enumerate(self.steps):
            print(u'{idx}: Executing step {step}'.format(step=step, idx=i + 1))
            step.execute(self.contract)
            users = [(u.relative_reputation(), u) for u in self.contract.users]
            users.sort(reverse=True)
            for rep, u in users[:5]:
                print('\tuser {user.id}: {rep}'.format(user=u, rep=rep))
            if len(users) > 10:
                print('\t.')
                print('\t.')
                for rep, u in users[-5:]:
                    print('\tuser {user.id}: {rep}'.format(user=u, rep=rep))
            else:
                for rep, u in users[5:]:
                    print('\tuser {user.id}: {rep}'.format(user=u, rep=rep))

            print('-' * 100)
