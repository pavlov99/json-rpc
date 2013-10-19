import json
import unittest

from ..jsonrpc2 import (
    JSONRPC20Request,
)


def isjsonequal(json1, json2):
    return json.loads(json1) == json.loads(json2)


class TestJSONRPC20Request(unittest.TestCase):

    """ Test JSONRPC20Request class."""

    def setUp(self):
        self.request_params = {
            "method": "add",
            "params": [1, 2],
            "_id": 1,
        }

    def test_correct_init(self):
        """ Test object is created."""
        JSONRPC20Request(**self.request_params)

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(ValueError):
            JSONRPC20Request()

    def test_method_validation_str(self):
        self.request_params.update({"method": "add"})
        JSONRPC20Request(**self.request_params)

    def test_method_validation_not_str(self):
        self.request_params.update({"method": []})
        with self.assertRaises(ValueError):
            JSONRPC20Request(**self.request_params)

        self.request_params.update({"method": {}})
        with self.assertRaises(ValueError):
            JSONRPC20Request(**self.request_params)

    def test_method_validation_str_rpc_prefix(self):
        """ Test method SHOULD NOT starts with rpc. """
        self.request_params.update({"method": "rpc."})
        with self.assertRaises(ValueError):
            JSONRPC20Request(**self.request_params)

        self.request_params.update({"method": "rpc.test"})
        with self.assertRaises(ValueError):
            JSONRPC20Request(**self.request_params)

        self.request_params.update({"method": "rpccorrect"})
        JSONRPC20Request(**self.request_params)

        self.request_params.update({"method": "rpc"})
        JSONRPC20Request(**self.request_params)

    def test_params_validation_list(self):
        self.request_params.update({"params": []})
        JSONRPC20Request(**self.request_params)

        self.request_params.update({"params": [0]})
        JSONRPC20Request(**self.request_params)

    def test_params_validation_tuple(self):
        self.request_params.update({"params": ()})
        JSONRPC20Request(**self.request_params)

        self.request_params.update({"params": tuple([0])})
        JSONRPC20Request(**self.request_params)

    def test_params_validation_dict(self):
        self.request_params.update({"params": {}})
        JSONRPC20Request(**self.request_params)

        self.request_params.update({"params": {"a": 0}})
        JSONRPC20Request(**self.request_params)

    def test_params_validation_none(self):
        self.request_params.update({"params": None})
        JSONRPC20Request(**self.request_params)

    def test_params_validation_incorrect(self):
        self.request_params.update({"params": "str"})
        with self.assertRaises(ValueError):
            JSONRPC20Request(**self.request_params)

    def test_request_args(self):
        self.assertEqual(JSONRPC20Request("add").args, ())
        self.assertEqual(JSONRPC20Request("add", []).args, ())
        self.assertEqual(JSONRPC20Request("add", {"a": 1}).args, ())
        self.assertEqual(JSONRPC20Request("add", [1, 2]).args, (1, 2))

    def test_request_kwargs(self):
        self.assertEqual(JSONRPC20Request("add").kwargs, {})
        self.assertEqual(JSONRPC20Request("add", [1, 2]).kwargs, {})
        self.assertEqual(JSONRPC20Request("add", {}).kwargs, {})
        self.assertEqual(JSONRPC20Request("add", {"a": 1}).kwargs, {"a": 1})

    def test_id_validation_string(self):
        self.request_params.update({"_id": "id"})
        JSONRPC20Request(**self.request_params)

    def test_id_validation_int(self):
        self.request_params.update({"_id": 0})
        JSONRPC20Request(**self.request_params)

    def test_id_validation_null(self):
        self.request_params.update({"_id": "null"})
        JSONRPC20Request(**self.request_params)

    def test_id_validation_none(self):
        self.request_params.update({"_id": None})
        JSONRPC20Request(**self.request_params)

    def test_id_validation_float(self):
        self.request_params.update({"_id": 0.1})
        with self.assertRaises(ValueError):
            JSONRPC20Request(**self.request_params)

    def test_id_validation_incorrect(self):
        self.request_params.update({"_id": []})
        with self.assertRaises(ValueError):
            JSONRPC20Request(**self.request_params)

        self.request_params.update({"_id": ()})
        with self.assertRaises(ValueError):
            JSONRPC20Request(**self.request_params)

    def test_dict_method_1(self):
        r = JSONRPC20Request("add")
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        })

    def test_dict_method_2(self):
        r = JSONRPC20Request(method="add")
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        })

    def test_dict_method_3(self):
        r = JSONRPC20Request("add", None)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        })

    def test_dict_params_1(self):
        r = JSONRPC20Request("add", params=None, _id=None)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        })

    def test_dict_params_2(self):
        r = JSONRPC20Request("add", [])
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_dict_params_3(self):
        r = JSONRPC20Request("add", ())
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_dict_params_4(self):
        r = JSONRPC20Request("add", (1, 2))
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [1, 2],
            "id": None,
        })

    def test_dict_params_5(self):
        r = JSONRPC20Request("add", {"a": 0})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": {"a": 0},
            "id": None,
        })

    def test_dict_id_1(self):
        r = JSONRPC20Request("add", _id="null")
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": "null",
        })

    def test_dict_id_1_notification(self):
        r = JSONRPC20Request("add", _id="null", is_notification=True)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_dict_id_2(self):
        r = JSONRPC20Request("add", _id=None)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        })

    def test_dict_id_2_notification(self):
        r = JSONRPC20Request("add", _id=None, is_notification=True)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_dict_id_3(self):
        r = JSONRPC20Request("add", _id="id")
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": "id",
        })

    def test_dict_id_3_notification(self):
        r = JSONRPC20Request("add", _id="id", is_notification=True)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_dict_id_4(self):
        r = JSONRPC20Request("add", _id=0)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": 0,
        })

    def test_dict_id_4_notification(self):
        r = JSONRPC20Request("add", _id=0, is_notification=True)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_is_notification(self):
        r = JSONRPC20Request("add")
        self.assertFalse(r.is_notification)

        r = JSONRPC20Request("add", _id=None)
        self.assertFalse(r.is_notification)

        r = JSONRPC20Request("add", _id="null")
        self.assertFalse(r.is_notification)

        r = JSONRPC20Request("add", _id=0)
        self.assertFalse(r.is_notification)

        r = JSONRPC20Request("add", is_notification=True)
        self.assertTrue(r.is_notification)

        r = JSONRPC20Request("add", is_notification=True, _id=None)
        self.assertTrue(r.is_notification)
        self.assertNotIn("id", r.data)

        r = JSONRPC20Request("add", is_notification=True, _id=0)
        self.assertTrue(r.is_notification)
        self.assertNotIn("id", r.data)

    def test_serialize_method_1(self):
        r = JSONRPC20Request("add")
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        }, json.loads(r.json))

    def test_serialize_method_2(self):
        r = JSONRPC20Request(method="add")
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        }, json.loads(r.json))

    def test_serialize_method_3(self):
        r = JSONRPC20Request("add", None)
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        }, json.loads(r.json))

    def test_serialize_params_1(self):
        r = JSONRPC20Request("add", params=None, _id=None)
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        }, json.loads(r.json))

    def test_serialize_params_2(self):
        r = JSONRPC20Request("add", [])
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
            "id": None,
        }, json.loads(r.json))

    def test_serialize_params_3(self):
        r = JSONRPC20Request("add", ())
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
            "id": None,
        }, json.loads(r.json))

    def test_serialize_params_4(self):
        r = JSONRPC20Request("add", (1, 2))
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "params": [1, 2],
            "id": None,
        }, json.loads(r.json))

    def test_serialize_params_5(self):
        r = JSONRPC20Request("add", {"a": 0})
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "params": {"a": 0},
            "id": None,
        }, json.loads(r.json))

    def test_serialize_id_1(self):
        r = JSONRPC20Request("add", _id="null")
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "id": "null",
        }, json.loads(r.json))

    def test_serialize_id_2(self):
        r = JSONRPC20Request("add", _id=None)
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        }, json.loads(r.json))

    def test_serialize_id_3(self):
        r = JSONRPC20Request("add", _id="id")
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "id": "id",
        }, json.loads(r.json))

    def test_serialize_id_4(self):
        r = JSONRPC20Request("add", _id=0)
        self.assertTrue({
            "jsonrpc": "2.0",
            "method": "add",
            "id": 0,
        }, json.loads(r.json))

    def test_from_json_request_no_id(self):
        str_json = json.dumps({
            "method": "add",
            "params": [1, 2],
            "jsonrpc": "2.0",
        })

        request = JSONRPC20Request.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPC20Request))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, [1, 2])
        self.assertEqual(request._id, None)
        self.assertTrue(request.is_notification)

    def test_from_json_request_no_params(self):
        str_json = json.dumps({
            "method": "add",
            "jsonrpc": "2.0",
        })

        request = JSONRPC20Request.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPC20Request))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, None)
        self.assertEqual(request._id, None)
        self.assertTrue(request.is_notification)

    def test_from_json_request_null_id(self):
        str_json = json.dumps({
            "method": "add",
            "jsonrpc": "2.0",
            "id": None,
        })

        request = JSONRPC20Request.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPC20Request))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, None)
        self.assertEqual(request._id, None)
        self.assertFalse(request.is_notification)

    def test_from_json_request(self):
        str_json = json.dumps({
            "method": "add",
            "params": [0, 1],
            "jsonrpc": "2.0",
            "id": "id",
        })

        request = JSONRPC20Request.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPC20Request))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, [0, 1])
        self.assertEqual(request._id, "id")
        self.assertFalse(request.is_notification)
