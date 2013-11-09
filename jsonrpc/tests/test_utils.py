""" Test utility functionality."""
import datetime
import decimal
import json
import unittest

from ..utils import JSONSerializable, DatetimeDecimalEncoder


class TestJSONSerializable(unittest.TestCase):

    """ Test JSONSerializable functionality."""

    def setUp(self):
        class A(JSONSerializable):
            @property
            def json(self):
                pass

            @classmethod
            def from_json(cls, self):
                pass

        self._class = A

    def test_abstract_class(self):
        with self.assertRaises(TypeError):
            JSONSerializable()

        self._class()

    def test_definse_serialize_deserialize(self):
        """ Test classmethods of inherited class."""
        self.assertEqual(self._class.serialize({}), "{}")
        self.assertEqual(self._class.deserialize("{}"), {})


class TestDatetimeDecimalEncoder(unittest.TestCase):

    """ Test DatetimeDecimalEncoder functionality."""

    def test_date_encoder(self):
        obj = datetime.date.today()

        with self.assertRaises(TypeError):
            json.dumps(obj)

        self.assertEqual(
            json.dumps(obj, cls=DatetimeDecimalEncoder),
            '"{}"'.format(obj.isoformat()),
        )

    def test_datetime_encoder(self):
        obj = datetime.datetime.now()

        with self.assertRaises(TypeError):
            json.dumps(obj)

        self.assertEqual(
            json.dumps(obj, cls=DatetimeDecimalEncoder),
            '"{}"'.format(obj.isoformat()),
        )

    def test_decimal_encoder(self):
        obj = decimal.Decimal(0.1)

        with self.assertRaises(TypeError):
            json.dumps(obj)

        self.assertEqual(
            json.dumps(obj, cls=DatetimeDecimalEncoder),
            "0.1")
