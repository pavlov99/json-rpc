import requests
import json


def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "echo",
        "params": ["echome!"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    assert response["result"] == "echome!"
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 0

    # Example add method
    payload = {
        "method": "add",
        "params": [1, 2],
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    assert response["result"] == 3
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 1

    # Example foobar method
    payload = {
        "method": "foobar",
        "params": {"foo": "json", "bar": "-rpc"},
        "jsonrpc": "2.0",
        "id": 3,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    assert response["result"] == "json-rpc"
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 3

    # Example exception
    payload = {
        "method": "add",
        "params": [0],
        "jsonrpc": "2.0",
        "id": 4,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    assert response["error"]["message"] == "Invalid params"
    assert response["error"]["code"] == -32602
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 4


if __name__ == "__main__":
    main()
