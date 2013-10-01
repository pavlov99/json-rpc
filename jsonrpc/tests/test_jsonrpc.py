import json
import unittest

from ..jsonrpc import JSONRPCRequest, JSONRPCBatchRequest


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
            {"method": "devide", "params": {"numerator": 1, "denominator": 2},
             "jsonrpc": "2.0"},
        )

    def test_request_args(self):
        self.assertEqual(JSONRPCRequest("add", []).args, ())
        self.assertEqual(JSONRPCRequest("add", {"a": 1}).args, ())
        self.assertEqual(JSONRPCRequest("add", [1, 2]).args, (1, 2))

    def test_request_kwargs(self):
        self.assertEqual(JSONRPCRequest("add", [1, 2]).kwargs, {})
        self.assertEqual(JSONRPCRequest("add", {}).kwargs, {})
        self.assertEqual(JSONRPCRequest("add", {"a": 1}).kwargs, {"a": 1})

    def test_batch_request(self):
        request = JSONRPCBatchRequest(
            JSONRPCRequest("devide", {"num": 1, "denom": 2}, _id=1),
            JSONRPCRequest("devide", {"num": 3, "denom": 2}, _id=2),
        )
        self.assertEqual(json.loads(request.json), [
            {"method": "devide", "params": {"num": 1, "denom": 2}, "id": 1,
             "jsonrpc": "2.0"},
            {"method": "devide", "params": {"num": 3, "denom": 2}, "id": 2,
             "jsonrpc": "2.0"},
        ])

    def test_deserialize(self):
        str_json = json.dumps({
            "method": "add",
            "params": [1, 2],
            "jsonrpc": "2.0",
        })

        request = JSONRPCRequest.from_json(str_json)
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, [1, 2])

    def test_batch_deserialize(self):
        str_json = json.dumps([
            {"method": "add", "params": [1, 2], "jsonrpc": "2.0"},
            {"method": "mul", "params": [1, 2], "jsonrpc": "2.0"},
        ])

        request = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(request, list))

    def test_respond_success(self):
        request = JSONRPCRequest("add", [1, 2])
        self.assertTrue(isjsonequal(
            request.respond_success(3),
            '{"jsonrpc": "2.0", "result": 3, "id": null}',
        ))

    def test_respond_success_with_id(self):
        request = JSONRPCRequest("add", [1, 2], "0")
        self.assertTrue(isjsonequal(
            request.respond_success(3),
            '{"jsonrpc": "2.0", "result": 3, "id": "0"}',
        ))
