""" Test Django Backend."""
from __future__ import absolute_import
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


from ..backend.django import JSONRPCAPI, api


class TestDjangoBackend(unittest.TestCase):
    def test_urls(self):
        self.assertTrue(isinstance(api.urls, list))
