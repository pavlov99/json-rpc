import json
import unittest

from ..jsonrpc import (
    JSONRPCRequest,
    JSONRPCBatchRequest,
    JSONRPCResponse,
    JSONRPCBatchResponse,
    JSONRPCResponseManager,
)


class TestJSONRPCBatchResponse(unittest.TestCase):
    def test_batch_response(self):
        response = JSONRPCBatchResponse(
            JSONRPCResponse(result="result", _id=1),
            JSONRPCResponse(error={"code": 0, "message": ""}, _id=2),
        )
        self.assertEqual(json.loads(response.json), [
            {"result": "result", "id": 1, "jsonrpc": "2.0"},
            {"error": {"code": 0, "message": ""}, "id": 2, "jsonrpc": "2.0"},
        ])

    def test_response_iterator(self):
        responses = JSONRPCBatchResponse(
            JSONRPCResponse(result="result", _id=1),
            JSONRPCResponse(result="result", _id=2),
        )
        for response in responses:
            self.assertTrue(isinstance(response, JSONRPCResponse))
            self.assertEqual(response.result, "result")

    def test_batch_response_dict(self):
        response = JSONRPCBatchResponse(
            JSONRPCResponse(result="result", _id=1),
            JSONRPCResponse(result="result", _id=2),
        )
        self.assertEqual(response._data, [
            {"id": 1, "jsonrpc": "2.0", "result": "result"},
            {"id": 2, "jsonrpc": "2.0", "result": "result"},
        ])


class TestJSONRPCResponseManager(unittest.TestCase):
    def setUp(self):
        def raise_(e):
            raise e

        self.dispatcher = {
            "add": sum,
            "list_len": len,
            "101_base": lambda **kwargs: int("101", **kwargs),
            "error": lambda: raise_(KeyError("error_explanation"))
        }

    def test_returned_type_response(self):
        request = JSONRPCRequest("add", [[]], _id=0)
        response = JSONRPCResponseManager.handle(request.json, self.dispatcher)
        self.assertTrue(isinstance(response, JSONRPCResponse))

    def test_returned_type_butch_response(self):
        request = JSONRPCBatchRequest(
            JSONRPCRequest("add", [[]], _id=0))
        response = JSONRPCResponseManager.handle(request.json, self.dispatcher)
        self.assertTrue(isinstance(response, JSONRPCBatchResponse))

    def test_parse_error(self):
        req = '{"jsonrpc": "2.0", "method": "foobar, "params": "bar", "baz]'
        response = JSONRPCResponseManager.handle(req, self.dispatcher)
        self.assertTrue(isinstance(response, JSONRPCResponse))
        self.assertEqual(response.error["message"], "Parse error")
        self.assertEqual(response.error["code"], -32700)

    def test_invalid_request(self):
        req = '{"jsonrpc": "2.0", "method": 1, "params": "bar"}'
        response = JSONRPCResponseManager.handle(req, self.dispatcher)
        self.assertTrue(isinstance(response, JSONRPCResponse))
        self.assertEqual(response.error["message"], "Invalid Request")
        self.assertEqual(response.error["code"], -32600)

    def test_method_not_found(self):
        request = JSONRPCRequest("does_not_exist", [[]], _id=0)
        response = JSONRPCResponseManager.handle(request.json, self.dispatcher)
        self.assertTrue(isinstance(response, JSONRPCResponse))
        self.assertEqual(response.error["message"], "Method not found")
        self.assertEqual(response.error["code"], -32601)

    def test_invalid_params(self):
        request = JSONRPCRequest("add", {"a": 0}, _id=0)
        response = JSONRPCResponseManager.handle(request.json, self.dispatcher)
        self.assertTrue(isinstance(response, JSONRPCResponse))
        self.assertEqual(response.error["message"], "Invalid params")
        self.assertEqual(response.error["code"], -32602)

    def test_server_error(self):
        request = JSONRPCRequest("error", _id=0)
        response = JSONRPCResponseManager.handle(request.json, self.dispatcher)
        self.assertTrue(isinstance(response, JSONRPCResponse))
        self.assertEqual(response.error["message"], "Server error")
        self.assertEqual(response.error["code"], -32000)
        self.assertEqual(response.error["data"], {
            "type": "KeyError",
            "args": ('error_explanation',),
            "message": "'error_explanation'",
        })
