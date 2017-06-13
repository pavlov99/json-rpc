""" Test Django Backend."""
from __future__ import absolute_import
import os

try:
    from django.core.urlresolvers import RegexURLPattern
    from django.test import TestCase
except ImportError:
    import unittest
    raise unittest.SkipTest('Django not found for testing')

from ...backend.django import JSONRPCAPI, api
import json


class TestDjangoBackend(TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['DJANGO_SETTINGS_MODULE'] = \
            'jsonrpc.tests.test_backend_django.settings'

    def test_urls(self):
        self.assertTrue(isinstance(api.urls, list))
        for api_url in api.urls:
            self.assertTrue(isinstance(api_url, RegexURLPattern))

    def assertValidResult(self, json_data, result=''):
        response = self.client.post(
            '',
            json.dumps(json_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf8'))
        self.assertEqual(data.get('error', ''), '')
        self.assertEqual(data['result'], result)

    def test_client_json_rpc_2_with_no_params(self):
        @api.dispatcher.add_method
        def dummy(*args, **kwargs):
            self.assertEqual(len(args), 0)
            self.assertEqual(len(kwargs), 1)
            self.assertIn('request', kwargs)
            return ""

        self.assertValidResult({
            "id": "0",
            "jsonrpc": "2.0",
            "method": "dummy",
        })

    def test_client_json_rpc_2_with_empty_param_dict(self):
        @api.dispatcher.add_method
        def dummy(*args, **kwargs):
            self.assertEqual(len(args), 0)
            self.assertEqual(len(kwargs), 1)
            self.assertIn('request', kwargs)
            return ""

        self.assertValidResult({
            "id": "0",
            "jsonrpc": "2.0",
            "method": "dummy",
            "params": {},
        })

    def test_client_json_rpc_2_with_empty_param_list(self):
        @api.dispatcher.add_method
        def dummy(*args, **kwargs):
            self.assertEqual(len(args), 0)
            self.assertEqual(len(kwargs), 1)
            self.assertIn('request', kwargs)
            return ""

        self.assertValidResult({
            "id": "0",
            "jsonrpc": "2.0",
            "method": "dummy",
            "params": [],
        })

    def test_client_json_rpc_1_with_single_param(self):
        @api.dispatcher.add_method
        def dummy(param1):
            return param1

        self.assertValidResult({
            "id": "0",
            "method": "dummy",
            "params": ['param1'],
        }, 'param1')

    def test_client_json_rpc_1_with_empty_params(self):
        @api.dispatcher.add_method
        def dummy(*args, **kwargs):
            self.assertEqual(len(args), 0)
            self.assertEqual(len(kwargs), 0)
            return ""

        self.assertValidResult({
            "id": "0",
            "method": "dummy",
            "params": [],
        })

    def test_method_not_allowed(self):
        response = self.client.get(
            '',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 405, "Should allow only POST")

    def test_invalid_request(self):
        response = self.client.post(
            '',
            '{',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf8'))
        self.assertEqual(data['error']['code'], -32700)
        self.assertEqual(data['error']['message'], 'Parse error')

    def test_resource_map(self):
        response = self.client.get('/map')
        self.assertEqual(response.status_code, 200)
        data = response.content.decode('utf8')
        self.assertIn("JSON-RPC map", data)

    def test_method_not_allowed_prefix(self):
        response = self.client.get(
            '/prefix',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 405)

    def test_resource_map_prefix(self):
        response = self.client.get('/prefix/map')
        self.assertEqual(response.status_code, 200)

    def test_empty_initial_dispatcher(self):
        class SubDispatcher(type(api.dispatcher)):
            pass

        custom_dispatcher = SubDispatcher()
        custom_api = JSONRPCAPI(custom_dispatcher)
        self.assertEqual(type(custom_api.dispatcher), SubDispatcher)
        self.assertEqual(id(custom_api.dispatcher), id(custom_dispatcher))
