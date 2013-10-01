import json
import unittest

from ..jsonrpc import (
    JSONRPCRequest,
    JSONRPCBatchRequest,
    JSONRPCResponse,
)
from ..exceptions import JSONRPCError


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

    def test_dict_method_1(self):
        r = JSONRPCRequest("add")
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_dict_method_2(self):
        r = JSONRPCRequest(method="add")
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_dict_method_3(self):
        r = JSONRPCRequest("add", None)
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_dict_params_1(self):
        r = JSONRPCRequest("add", params=None, _id=None)
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_dict_params_2(self):
        r = JSONRPCRequest("add", [])
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
        })

    def test_dict_params_3(self):
        r = JSONRPCRequest("add", ())
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
        })

    def test_dict_params_4(self):
        r = JSONRPCRequest("add", (1, 2))
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [1, 2],
        })

    def test_dict_params_5(self):
        r = JSONRPCRequest("add", {"a": 0})
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": {"a": 0},
        })

    def test_dict_id_1(self):
        r = JSONRPCRequest("add", _id="null")
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": "null",
        })

    def test_dict_id_2(self):
        r = JSONRPCRequest("add", _id=None)
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_dict_id_3(self):
        r = JSONRPCRequest("add", _id="id")
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": "id",
        })

    def test_dict_id_4(self):
        r = JSONRPCRequest("add", _id=0)
        self.assertEqual(r._dict, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": 0,
        })

    def test_is_notification(self):
        r = JSONRPCRequest("add")
        self.assertTrue(r.is_notification)

        r = JSONRPCRequest("add", _id=None)
        self.assertTrue(r.is_notification)

        r = JSONRPCRequest("add", _id="null")
        self.assertFalse(r.is_notification)

        r = JSONRPCRequest("add", _id=0)
        self.assertFalse(r.is_notification)

    def test_serialize_method_1(self):
        r = JSONRPCRequest("add")
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
        }))

    def test_serialize_method_2(self):
        r = JSONRPCRequest(method="add")
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
        }))

    def test_serialize_method_3(self):
        r = JSONRPCRequest("add", None)
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
        }))

    def test_serialize_params_1(self):
        r = JSONRPCRequest("add", params=None, _id=None)
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
        }))

    def test_serialize_params_2(self):
        r = JSONRPCRequest("add", [])
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
        }))

    def test_serialize_params_3(self):
        r = JSONRPCRequest("add", ())
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
        }))

    def test_serialize_params_4(self):
        r = JSONRPCRequest("add", (1, 2))
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
            "params": [1, 2],
        }))

    def test_serialize_params_5(self):
        r = JSONRPCRequest("add", {"a": 0})
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
            "params": {"a": 0},
        }))

    def test_serialize_id_1(self):
        r = JSONRPCRequest("add", _id="null")
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
            "id": "null",
        }))

    def test_serialize_id_2(self):
        r = JSONRPCRequest("add", _id=None)
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
        }))

    def test_serialize_id_3(self):
        r = JSONRPCRequest("add", _id="id")
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
            "id": "id",
        }))

    def test_serialize_id_4(self):
        r = JSONRPCRequest("add", _id=0)
        self.assertEqual(r.json, json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
            "id": 0,
        }))

    def test_from_json_request_no_id(self):
        str_json = json.dumps({
            "method": "add",
            "params": [1, 2],
            "jsonrpc": "2.0",
        })

        request = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPCRequest))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, [1, 2])
        self.assertEqual(request._id, None)

    def test_from_json_request_no_params(self):
        str_json = json.dumps({
            "method": "add",
            "jsonrpc": "2.0",
        })

        request = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPCRequest))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, None)
        self.assertEqual(request._id, None)

    def test_from_json_request(self):
        str_json = json.dumps({
            "method": "add",
            "params": [0, 1],
            "jsonrpc": "2.0",
            "id": "id",
        })

        request = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPCRequest))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, [0, 1])
        self.assertEqual(request._id, "id")

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


class TestJSONRPCBatchRequest(unittest.TestCase):
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

    def test_from_json_batch(self):
        str_json = json.dumps([
            {"method": "add", "params": [1, 2], "jsonrpc": "2.0"},
            {"method": "mul", "params": [1, 2], "jsonrpc": "2.0"},
        ])

        requests = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(requests, list))
        for r in requests:
            self.assertTrue(isinstance(r, JSONRPCRequest))
            self.assertTrue(r.method in ["add", "mul"])
            self.assertEqual(r.params, [1, 2])
            self.assertEqual(r._id, None)


class TestJSONRPCError(unittest.TestCase):
    def setUp(self):
        self.error_params = {
            "code": 0,
            "message": "",
        }

    def test_correct_init(self):
        """ Test object is created."""
        JSONRPCError(**self.error_params)

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(ValueError):
            JSONRPCError()

    def test_code_validation_int(self):
        self.error_params.update({"code": 32000})
        JSONRPCError(**self.error_params)

    def test_code_validation_no_code(self):
        del self.error_params["code"]
        with self.assertRaises(ValueError):
            JSONRPCError(**self.error_params)

    def test_code_validation_str(self):
        self.error_params.update({"code": "0"})
        with self.assertRaises(ValueError):
            JSONRPCError(**self.error_params)

    def test_message_validation_str(self):
        self.error_params.update({"message": ""})
        JSONRPCError(**self.error_params)

    def test_message_validation_none(self):
        del self.error_params["message"]
        with self.assertRaises(ValueError):
            JSONRPCError(**self.error_params)

    def test_message_validation_int(self):
        self.error_params.update({"message": 0})
        with self.assertRaises(ValueError):
            JSONRPCError(**self.error_params)


class TestJSONRPCResponse(unittest.TestCase):
    def setUp(self):
        self.response_success_params = {
            "result": "",
            "_id": 1,
        }
        self.response_error_params = {
            "error": {
                "code": 1,
                "message": "error",
            },
            "_id": 1,
        }

    def test_correct_init(self):
        """ Test object is created."""
        JSONRPCResponse(**self.response_success_params)

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(ValueError):
            JSONRPCResponse()

    def test_validation_incorrect_result_and_error(self):
        with self.assertRaises(ValueError):
            JSONRPCResponse(result="", error={"code": 1, "message": ""})

    #def test_method_validation_str(self):
        #self.request_params.update({"method": "add"})
        #JSONRPCRequest(**self.request_params)

    #def test_method_validation_not_str(self):
        #self.request_params.update({"method": []})
        #with self.assertRaises(ValueError):
            #JSONRPCRequest(**self.request_params)

        #self.request_params.update({"method": {}})
        #with self.assertRaises(ValueError):
            #JSONRPCRequest(**self.request_params)
