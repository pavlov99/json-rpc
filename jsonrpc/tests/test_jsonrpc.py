import json
import unittest

from ..jsonrpc import (
    JSONRPCRequest,
    JSONRPCBatchRequest,
    JSONRPCResponse,
    JSONRPCBatchResponse,
    JSONRPCResponseManager,
)
from ..exceptions import (
    JSONRPCError,
    JSONRPCInternalError,
    JSONRPCInvalidParams,
    JSONRPCInvalidRequest,
    JSONRPCMethodNotFound,
    JSONRPCParseError,
    JSONRPCServerError,
)


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

    def test_from_json_batch_one(self):
        str_json = json.dumps([
            {"method": "add", "params": [1, 2], "jsonrpc": "2.0"},
        ])

        requests = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(requests, list))
        self.assertEqual(len(requests), 1)
        r = requests[0]
        self.assertTrue(isinstance(r, JSONRPCRequest))
        self.assertEqual(r.method, "add")
        self.assertEqual(r.params, [1, 2])
        self.assertEqual(r._id, None)

    def test_response_iterator(self):
        requests = JSONRPCBatchRequest(
            JSONRPCRequest("devide", {"num": 1, "denom": 2}, _id=1),
            JSONRPCRequest("devide", {"num": 3, "denom": 2}, _id=2),
        )
        for request in requests:
            self.assertTrue(isinstance(request, JSONRPCRequest))
            self.assertEqual(request.method, "devide")


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
        self.assertEqual(response._dict, [
            {"id": 1, "jsonrpc": "2.0", "result": "result"},
            {"id": 2, "jsonrpc": "2.0", "result": "result"},
        ])


class TestJSONRPCResponseManager(unittest.TestCase):
    def setUp(self):
        self.dispatcher = {
            "add": sum,
            "list_len": len,
            "101_base": lambda **kwargs: int("101", **kwargs),
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

    def test_data_validation_none(self):
        self.error_params.update({"data": None})
        JSONRPCError(**self.error_params)

    def test_data_validation(self):
        self.error_params.update({"data": {}})
        JSONRPCError(**self.error_params)

        self.error_params.update({"data": ""})
        JSONRPCError(**self.error_params)

    def test_from_json(self):
        str_json = json.dumps({
            "code": 0,
            "message": "",
            "data": {},
        })

        request = JSONRPCError.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPCError))
        self.assertEqual(request.code, 0)
        self.assertEqual(request.message, "")
        self.assertEqual(request.data, {})


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

    def test_validation_error_correct(self):
        JSONRPCResponse(**self.response_error_params)

    def test_validation_error_incorrect(self):
        self.response_error_params["error"].update({"code": "str"})
        with self.assertRaises(ValueError):
            JSONRPCResponse(**self.response_error_params)

    def test_validation_error_incorrect_no_code(self):
        del self.response_error_params["error"]["code"]
        with self.assertRaises(ValueError):
            JSONRPCResponse(**self.response_error_params)

    def test_validation_error_incorrect_no_message(self):
        del self.response_error_params["error"]["message"]
        with self.assertRaises(ValueError):
            JSONRPCResponse(**self.response_error_params)

    def test_validation_error_incorrect_message_not_str(self):
        self.response_error_params["error"].update({"message": 0})
        with self.assertRaises(ValueError):
            JSONRPCResponse(**self.response_error_params)


class TestJSONRPCParseError(unittest.TestCase):
    def test_code_message(self):
        error = JSONRPCParseError()
        self.assertEqual(error.code, -32700)
        self.assertEqual(error.message, "Parse error")
        self.assertEqual(error.data, None)


class TestJSONRPCServerError(unittest.TestCase):
    def test_code_message(self):
        error = JSONRPCServerError()
        self.assertEqual(error.code, -32000)
        self.assertEqual(error.message, "Server error")
        self.assertEqual(error.data, None)


class TestJSONRPCInternalError(unittest.TestCase):
    def test_code_message(self):
        error = JSONRPCInternalError()
        self.assertEqual(error.code, -32603)
        self.assertEqual(error.message, "Internal error")
        self.assertEqual(error.data, None)


class TestJSONRPCInvalidParams(unittest.TestCase):
    def test_code_message(self):
        error = JSONRPCInvalidParams()
        self.assertEqual(error.code, -32602)
        self.assertEqual(error.message, "Invalid params")
        self.assertEqual(error.data, None)


class TestJSONRPCInvalidRequest(unittest.TestCase):
    def test_code_message(self):
        error = JSONRPCInvalidRequest()
        self.assertEqual(error.code, -32600)
        self.assertEqual(error.message, "Invalid Request")
        self.assertEqual(error.data, None)


class TestJSONRPCMethodNotFound(unittest.TestCase):
    def test_code_message(self):
        error = JSONRPCMethodNotFound()
        self.assertEqual(error.code, -32601)
        self.assertEqual(error.message, "Method not found")
        self.assertEqual(error.data, None)
