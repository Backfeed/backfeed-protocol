import unittest
import protocol
from protocol.contracts.dmag import DMagContract


class GetContractTestCase(unittest.TestCase):
    """tests for protocol.get_contract"""

    def test_get_contract(self):

        contract = protocol.get_contract()
        self.assertTrue(isinstance(contract, DMagContract))
