import backfeed_protocol
from ..contracts.dmag import DMagContract
from ..contracts.example import ExampleContract
from common import TestCase


class GetContractTestCase(TestCase):
    """tests for protocol.get_contract"""

    def test_get_contract(self):

        contract0 = backfeed_protocol.utils.get_contract(u'example')
        contract1 = backfeed_protocol.utils.get_contract(u'dmag')
        contract2 = backfeed_protocol.utils.get_contract(u'dmag')
        contract3 = backfeed_protocol.utils.get_contract(u'example')

        self.assertEqual(contract0, contract3)
        self.assertEqual(contract1, contract2)
        self.assertTrue(isinstance(contract0, ExampleContract))
        self.assertTrue(isinstance(contract1, DMagContract))
