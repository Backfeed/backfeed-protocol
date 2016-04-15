import unittest
import backfeed_protocol
from ..contracts.dmag import DMagContract


class GetContractTestCase(unittest.TestCase):
    """tests for protocol.get_contract"""

    def test_get_contract(self):

        contract = backfeed_protocol.get_contract()
        self.assertTrue(isinstance(contract, DMagContract))
