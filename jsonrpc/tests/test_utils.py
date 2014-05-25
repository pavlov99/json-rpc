""" Test utility functionality."""
import datetime
import decimal
import json
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from mock import patch

from ..utils import JSONSerializable, DatetimeDecimalEncoder


class TestJSONSerializable(unittest.TestCase):

    """ Test JSONSerializable functionality."""

    def setUp(self):
        class A(JSONSerializable):
            @property
            def json(self):
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

    def test_from_json(self):
        self.assertTrue(isinstance(self._class.from_json('{}'), self._class))

    def test_from_json_incorrect(self):
        with self.assertRaises(ValueError):
            self._class.from_json('[]')


class TestDatetimeDecimalEncoder(unittest.TestCase):

    """ Test DatetimeDecimalEncoder functionality."""

    def test_date_encoder(self):
        obj = datetime.date.today()

        with self.assertRaises(TypeError):
            json.dumps(obj)

        self.assertEqual(
            json.dumps(obj, cls=DatetimeDecimalEncoder),
            '"{0}"'.format(obj.isoformat()),
        )

    def test_datetime_encoder(self):
        obj = datetime.datetime.now()

        with self.assertRaises(TypeError):
            json.dumps(obj)

        self.assertEqual(
            json.dumps(obj, cls=DatetimeDecimalEncoder),
            '"{0}"'.format(obj.isoformat()),
        )

    def test_decimal_encoder(self):
        obj = decimal.Decimal('0.1')

        with self.assertRaises(TypeError):
            json.dumps(obj)

        result = json.dumps(obj, cls=DatetimeDecimalEncoder)
        self.assertTrue(isinstance(result, str))
        self.assertEqual(float(result), float(0.1))

    def test_default(self):
        encoder = DatetimeDecimalEncoder()
        with patch.object(json.JSONEncoder, 'default') as json_default:
            encoder.default("")

        self.assertEqual(json_default.call_count, 1)
