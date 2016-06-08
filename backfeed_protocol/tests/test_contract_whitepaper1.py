from ..contracts.whitepaper1 import WhitePaper1Contract

from test_contract_base import BaseContractTestCase


class WhitePaper1ContractTest(BaseContractTestCase):
    """test dmag protocol"""
    contract_class_to_test = WhitePaper1Contract
    contract_name = u'dmag'

    # Test contribution types
    def test_sanity(self,):
        contract = self.get_fresh_contract()
        contributor1 = contract.create_user()
        evaluator1 = contract.create_user()
        evaluator2 = contract.create_user()
        evaluator3 = contract.create_user()

        initial_total_reputation = contract.total_reputation()
        contribution = contract.create_contribution(user=contributor1)

        # on the first evaluation, nothing changes
        contract.create_evaluation(user=evaluator1, contribution=contribution, value=True)
        self.assertEqual(initial_total_reputation, contract.total_reputation())
        # evaluator 2 evaluates differently, and nothing changes again
        contract.create_evaluation(user=evaluator2, contribution=contribution, value=False)
        # on the third evaluation, some rep should flow to evaluator1
        contract.create_evaluation(user=evaluator3, contribution=contribution, value=True)

        self.assertEqual(initial_total_reputation, contract.total_reputation())
