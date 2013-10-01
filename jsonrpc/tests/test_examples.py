""" Exmples of usage with tests.

Tests in this file represent examples taken from JSON-RPC specification.
http://www.jsonrpc.org/specification#examples

"""
import unittest
import json
from ..jsonrpc import JSONRPCResponseManager


def isjsonequal(json1, json2):
    return json.loads(json1) == json.loads(json2)


class TestJSONRPCExamples(unittest.TestCase):
    def setUp(self):
        self.dispatcher = {
            "subtract": lambda a, b: a - b,
        }

    def test_rpc_call_with_positional_parameters(self):
        req = '{"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}'  # noqa
        response = JSONRPCResponseManager.handle(req, self.dispatcher)
        self.assertEqual(
            response.json,
            '{"jsonrpc": "2.0", "result": 19, "id": 1}'
        )

        req = '{"jsonrpc": "2.0", "method": "subtract", "params": [23, 42], "id": 2}'  # noqa
        response = JSONRPCResponseManager.handle(req, self.dispatcher)
        self.assertEqual(
            response.json,
            '{"jsonrpc": "2.0", "result": -19, "id": 2}'
        )

    def test_rpc_call_with_named_parameters(self):
        def subtract(minuend=None, subtrahend=None):
            return minuend - subtrahend

        dispatcher = {
            "subtract": subtract,
        }

        req = '{"jsonrpc": "2.0", "method": "subtract", "params": {"subtrahend": 23, "minuend": 42}, "id": 3}'  # noqa
        response = JSONRPCResponseManager.handle(req, dispatcher)
        self.assertEqual(
            response.json,
            '{"jsonrpc": "2.0", "result": 19, "id": 3}'
        )

        req = '{"jsonrpc": "2.0", "method": "subtract", "params": {"minuend": 42, "subtrahend": 23}, "id": 4}'  # noqa
        response = JSONRPCResponseManager.handle(req, dispatcher)
        self.assertEqual(
            response.json,
            '{"jsonrpc": "2.0", "result": 19, "id": 4}',
        )

    def test_notification(self):
        req = '{"jsonrpc": "2.0", "method": "update", "params": [1,2,3,4,5]}'
        response = JSONRPCResponseManager.handle(req, self.dispatcher)
        self.assertEqual(response, None)

        req = '{"jsonrpc": "2.0", "method": "foobar"}'
        response = JSONRPCResponseManager.handle(req, self.dispatcher)
        self.assertEqual(response, None)