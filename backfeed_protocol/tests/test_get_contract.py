import backfeed_protocol
from ..contracts.dmag import DMagContract
from common import TestCase


class GetContractTestCase(TestCase):
    """tests for protocol.get_contract"""

    def test_get_contract(self):

        contract = backfeed_protocol.utils.get_contract()
        self.assertTrue(isinstance(contract, DMagContract))
        contract2 = backfeed_protocol.utils.get_contract()
        self.assertEqual(contract, contract2)
