import json
import unittest

from ..jsonrpc import JSONRPCRequest, JSONRPCBatchRequest


def isjsonequal(json1, json2):
    return json.loads(json1) == json.loads(json2)


class TestJSONRPCRequest(unittest.TestCase):

    """ Test JSONRPCRequest class."""

    def setUp(self):
        self.request_params = {
            "method": "add",
            "params": [1, 2],
            "_id": 1,
        }

    def test_correct_init(self):
        """ Test object is created."""
        JSONRPCRequest(**self.request_params)

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(ValueError):
            JSONRPCRequest()

    def test_method_validation_str(self):
        self.request_params.update({"method": "add"})
        JSONRPCRequest(**self.request_params)

    def test_method_validation_not_str(self):
        self.request_params.update({"method": []})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

        self.request_params.update({"method": {}})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

    def test_method_validation_str_rpc_prefix(self):
        """ Test method SHOULD NOT starts with rpc. """
        self.request_params.update({"method": "rpc."})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

        self.request_params.update({"method": "rpc.test"})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

        self.request_params.update({"method": "rpccorrect"})
        JSONRPCRequest(**self.request_params)

        self.request_params.update({"method": "rpc"})
        JSONRPCRequest(**self.request_params)

    def test_params_validation_list(self):
        self.request_params.update({"params": []})
        JSONRPCRequest(**self.request_params)

        self.request_params.update({"params": [0]})
        JSONRPCRequest(**self.request_params)

    def test_params_validation_tuple(self):
        self.request_params.update({"params": ()})
        JSONRPCRequest(**self.request_params)

        self.request_params.update({"params": tuple([0])})
        JSONRPCRequest(**self.request_params)

    def test_params_validation_dict(self):
        self.request_params.update({"params": {}})
        JSONRPCRequest(**self.request_params)

        self.request_params.update({"params": {"a": 0}})
        JSONRPCRequest(**self.request_params)

    def test_params_validation_mone(self):
        self.request_params.update({"params": None})
        JSONRPCRequest(**self.request_params)

    def test_params_validation_incorrect(self):
        self.request_params.update({"params": "str"})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

    def test_request_args(self):
        self.assertEqual(JSONRPCRequest("add").args, ())
        self.assertEqual(JSONRPCRequest("add", []).args, ())
        self.assertEqual(JSONRPCRequest("add", {"a": 1}).args, ())
        self.assertEqual(JSONRPCRequest("add", [1, 2]).args, (1, 2))

    def test_request_kwargs(self):
        self.assertEqual(JSONRPCRequest("add").kwargs, {})
        self.assertEqual(JSONRPCRequest("add", [1, 2]).kwargs, {})
        self.assertEqual(JSONRPCRequest("add", {}).kwargs, {})
        self.assertEqual(JSONRPCRequest("add", {"a": 1}).kwargs, {"a": 1})

    def test_id_validation_string(self):
        self.request_params.update({"_id": "id"})
        JSONRPCRequest(**self.request_params)

    def test_id_validation_int(self):
        self.request_params.update({"_id": 0})
        JSONRPCRequest(**self.request_params)

    def test_id_validation_null(self):
        self.request_params.update({"_id": "null"})
        JSONRPCRequest(**self.request_params)

    def test_id_validation_none(self):
        self.request_params.update({"_id": None})
        JSONRPCRequest(**self.request_params)

    def test_id_validation_float(self):
        self.request_params.update({"_id": 0.1})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

    def test_id_validation_incorrect(self):
        self.request_params.update({"_id": []})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

        self.request_params.update({"_id": ()})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

    #def test_serialize_args_no_id(self):
        #request = JSONRPCRequest("add", [1, 2])
        #self.assertEqual(
            #json.loads(request.json),
            #{"method": "add", "params": [1, 2], "jsonrpc": "2.0"},
        #)

    #def test_serialize_kwargs_no_id(self):
        #request = JSONRPCRequest("devide", {"numerator": 1, "denominator": 2})
        #self.assertEqual(
            #json.loads(request.json),
            #{"method": "devide", "params": {"numerator": 1, "denominator": 2},
             #"jsonrpc": "2.0"},
        #)


    #def test_batch_request(self):
        #request = JSONRPCBatchRequest(
            #JSONRPCRequest("devide", {"num": 1, "denom": 2}, _id=1),
            #JSONRPCRequest("devide", {"num": 3, "denom": 2}, _id=2),
        #)
        #self.assertEqual(json.loads(request.json), [
            #{"method": "devide", "params": {"num": 1, "denom": 2}, "id": 1,
             #"jsonrpc": "2.0"},
            #{"method": "devide", "params": {"num": 3, "denom": 2}, "id": 2,
             #"jsonrpc": "2.0"},
        #])

    #def test_deserialize(self):
        #str_json = json.dumps({
            #"method": "add",
            #"params": [1, 2],
            #"jsonrpc": "2.0",
        #})

        #request = JSONRPCRequest.from_json(str_json)
        #self.assertEqual(request.method, "add")
        #self.assertEqual(request.params, [1, 2])

    #def test_batch_deserialize(self):
        #str_json = json.dumps([
            #{"method": "add", "params": [1, 2], "jsonrpc": "2.0"},
            #{"method": "mul", "params": [1, 2], "jsonrpc": "2.0"},
        #])

        #request = JSONRPCRequest.from_json(str_json)
        #self.assertTrue(isinstance(request, list))

    #def test_respond_success(self):
        #request = JSONRPCRequest("add", [1, 2])
        #self.assertTrue(isjsonequal(
            #request.respond_success(3),
            #'{"jsonrpc": "2.0", "result": 3, "id": null}',
        #))

    #def test_respond_success_with_id(self):
        #request = JSONRPCRequest("add", [1, 2], "0")
        #self.assertTrue(isjsonequal(
            #request.respond_success(3),
            #'{"jsonrpc": "2.0", "result": 3, "id": "0"}',
        #))
