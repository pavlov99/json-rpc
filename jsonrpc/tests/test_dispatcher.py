from ..dispatcher import Dispatcher
import unittest


class TestDispatcher(unittest.TestCase):

    """ Test Dispatcher functionality."""

    def test_getter(self):
        d = Dispatcher()

        with self.assertRaises(KeyError):
            d["method"]

        d["add"] = lambda *args: sum(args)
        self.assertEqual(d["add"](1, 1), 2)

    def test_in(self):
        d = Dispatcher()
        d["method"] = lambda: ""
        self.assertIn("method", d)

    def test_add_method(self):
        d = Dispatcher()

        @d.add_method
        def add(x, y):
            return x + y

        self.assertIn("add", d)
        self.assertEqual(d["add"](1, 1), 2)

    def test_del_method(self):
        d = Dispatcher()
        d["method"] = lambda: ""
        self.assertIn("method", d)

        del d["method"]
        self.assertNotIn("method", d)

    def test_to_dict(self):
        d = Dispatcher()
        func = lambda: ""
        d["method"] = func
        self.assertEqual(dict(d), {"method": func})
