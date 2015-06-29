import json
from unittest import TestCase

from flask import Blueprint, Flask

from ...backend.flask import api


@api.dispatcher.add_method
def dummy():
    return ""


class TestFlaskBackend(TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.register_blueprint(api.as_blueprint())
        self.client = app.test_client()

    def test_client(self):
        json_data = {
            "id": "0",
            "jsonrpc": "2.0",
            "method": "dummy",
        }
        response = self.client.post(
            '/',
            data=json.dumps(json_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf8'))
        self.assertEqual(data['result'], '')

    def test_method_not_allowed(self):
        response = self.client.get(
            '/',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 405, "Should allow only POST")

    def test_parse_error(self):
        response = self.client.post(
            '/',
            data='{',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf8'))
        self.assertEqual(data['error']['code'], -32700)
        self.assertEqual(data['error']['message'], 'Parse error')

    def test_invalid_request(self):
        response = self.client.post(
            '/',
            data='{"method": "dummy", "id": 1}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf8'))
        self.assertEqual(data['error']['code'], -32600)
        self.assertEqual(data['error']['message'], 'Invalid Request')

    def test_method_not_found(self):
        data = {
            "jsonrpc": "2.0",
            "method": "dummy2",
            "id": 1
        }
        response = self.client.post(
            '/',
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf8'))
        self.assertEqual(data['error']['code'], -32601)
        self.assertEqual(data['error']['message'], 'Method not found')

    def test_invalid_parameters(self):
        data = {
            "jsonrpc": "2.0",
            "method": "dummy",
            "params": [42],
            "id": 1
        }
        response = self.client.post(
            '/',
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf8'))
        self.assertEqual(data['error']['code'], -32602)
        self.assertEqual(data['error']['message'], 'Invalid params')

    def test_resource_map(self):
        response = self.client.get('/map')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("JSON-RPC map" in response.data.decode('utf8'))

    def test_method_not_allowed_prefix(self):
        response = self.client.get(
            '/',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 405)

    def test_resource_map_prefix(self):
        response = self.client.get('/map')
        self.assertEqual(response.status_code, 200)
