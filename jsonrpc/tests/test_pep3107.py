import unittest
from manager import JSONRPCResponseManager


class TestJSONRPCResponseManager(unittest.TestCase):
    def test_typeerror_with_annotations(self):
        """If a function has Python3 annotations and is called with improper
        arguments, make sure the framework doesn't fail with inspect.getargspec
        """
        def distance(a: float, b: float) -> float:
            return (a**2 + b**2)**0.5

        dispatcher = {
            "distance": distance,
        }

        req = '{"jsonrpc": "2.0", "method": "distance", "params": [], "id": 3}'  # noqa
        result = JSONRPCResponseManager.handle(req, dispatcher)

        # Make sure this returns JSONRPCInvalidParams rather than raising
        # UnboundLocalError
        self.assertEqual(result.error['code'], -32602)

