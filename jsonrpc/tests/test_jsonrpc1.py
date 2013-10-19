import json
import unittest

from ..jsonrpc1 import (
    JSONRPC10Request,
    JSONRPC10Response,
)


class TestJSONRPC10Request(unittest.TestCase):

    """ Test JSONRPC10Request functionality."""

    def setUp(self):
        self.request_params = {
            "method": "add",
            "params": [1, 2],
            "_id": 1,
        }

    def test_correct_init(self):
        """ Test object is created."""
        JSONRPC10Request(**self.request_params)

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(ValueError):
            JSONRPC10Request()

    def test_method_validation_str(self):
        self.request_params.update({"method": "add"})
        JSONRPC10Request(**self.request_params)

    def test_method_validation_not_str(self):
        self.request_params.update({"method": []})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

        self.request_params.update({"method": {}})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

        self.request_params.update({"method": None})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

    def test_params_validation_list(self):
        self.request_params.update({"params": []})
        JSONRPC10Request(**self.request_params)

        self.request_params.update({"params": [0]})
        JSONRPC10Request(**self.request_params)

    def test_params_validation_tuple(self):
        self.request_params.update({"params": ()})
        JSONRPC10Request(**self.request_params)

        self.request_params.update({"params": tuple([0])})
        JSONRPC10Request(**self.request_params)

    def test_params_validation_dict(self):
        self.request_params.update({"params": {}})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

        self.request_params.update({"params": {"a": 0}})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

    def test_params_validation_none(self):
        self.request_params.update({"params": None})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

    def test_params_validation_incorrect(self):
        self.request_params.update({"params": "str"})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

    def test_request_args(self):
        self.assertEqual(JSONRPC10Request("add").args, ())
        self.assertEqual(JSONRPC10Request("add", []).args, ())
        self.assertEqual(JSONRPC10Request("add", {"a": 1}).args, ())
        self.assertEqual(JSONRPC10Request("add", [1, 2]).args, (1, 2))

    def test_id_validation_string(self):
        self.request_params.update({"_id": "id"})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_int(self):
        self.request_params.update({"_id": 0})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_null(self):
        self.request_params.update({"_id": "null"})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_none(self):
        self.request_params.update({"_id": None})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_float(self):
        self.request_params.update({"_id": 0.1})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

    def test_id_validation_list_tuple(self):
        self.request_params.update({"_id": []})
        JSONRPC10Request(**self.request_params)

        self.request_params.update({"_id": ()})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_default_id_none(self):
        del self.request_params["_id"]
        JSONRPC10Request(**self.request_params)


class TestJSONRPC10Response(unittest.TestCase):

    """ Test JSONRPC10Response functionality."""
