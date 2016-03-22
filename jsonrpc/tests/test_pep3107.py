import unittest
import sys
from manager import JSONRPCResponseManager

if sys.version_info[0] < 3:
    sys.exit(0)

from p3_test_code import distance

class TestJSONRPCResponseManager(unittest.TestCase):
    def test_typeerror_with_annotations(self):
        """If a function has Python3 annotations and is called with improper
        arguments, make sure the framework doesn't fail with inspect.getargspec
        """

        dispatcher = {
            "distance": distance,
        }

        req = '{"jsonrpc": "2.0", "method": "distance", "params": [], "id": 3}'  # noqa
        result = JSONRPCResponseManager.handle(req, dispatcher)

        # Make sure this returns JSONRPCInvalidParams rather than raising
        # UnboundLocalError
        self.assertEqual(result.error['code'], -32602)

