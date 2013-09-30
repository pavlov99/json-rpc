import json
import unittest

from ..jsonrpc import JSONRPCRequest


def isjsonequal(json1, json2):
    return json.loads(json1) == json.loads(json2)


class TestJSONRPCRequest(unittest.TestCase):

    """ Test JSONRPCRequest class."""

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(Exception):
            JSONRPCRequest()

    def test_validation_incorrect_only_method(self):
        with self.assertRaises(Exception):
            JSONRPCRequest("add")

    def test_serialize_args_no_id(self):
        request = JSONRPCRequest("add", [1, 2])
        self.assertEqual(
            json.loads(request.json),
            {"method": "add", "params": [1, 2], "jsonrpc": "2.0"},
        )

    def test_serialize_kwargs_no_id(self):
        request = JSONRPCRequest("devide", {"numerator": 1, "denominator": 2})
        self.assertEqual(
            json.loads(request.json),
            {"method": "add", "params": {"numerator": 1, "denominator": 2},
             "jsonrpc": "2.0"},
        )
