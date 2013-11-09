json-rpc
========

[![Build Status](https://travis-ci.org/pavlov99/json-rpc.png?branch=master)](https://travis-ci.org/pavlov99/json-rpc)
[![Coverage Status](https://coveralls.io/repos/pavlov99/json-rpc/badge.png)](https://coveralls.io/r/pavlov99/json-rpc)
[![Downloads](https://pypip.in/v/json-rpc/badge.png)](https://crate.io/packages/json-rpc)
[![Downloads](https://pypip.in/d/json-rpc/badge.png)](https://crate.io/packages/json-rpc)

[JSON-RPC2.0](http://www.jsonrpc.org/specification) and [JSON-RPC1.0](http://json-rpc.org/wiki/specification) transport specification implementation. Supports python2.6+, python3.2+.

Documentation: http://json-rpc.readthedocs.org

This implementation does not have any transport functionality realization, only protocol.
Any client or server realization is easy based on current code, but requires transport libraries, such as requests, gevent or zmq, see [examples](https://github.com/pavlov99/json-rpc/tree/master/examples) directory.

Install
-------

    pip install json-rpc

Tests
-----

    tox

Quickstart
----------
Server (uses [Werkzeug](http://werkzeug.pocoo.org/))

    from werkzeug.wrappers import Request, Response
    from werkzeug.serving import run_simple

    from jsonrpc import JSONRPCResponseManager, dispatcher


    @dispatcher.add_method
    def foobar(**kwargs):
        return kwargs["foo"] + kwargs["bar"]


    @Request.application
    def application(request):
        # Dispatcher is dictionary {<method_name>: callable}
        dispatcher["echo"] = lambda s: s
        dispatcher["add"] = lambda a, b: a + b

        response = JSONRPCResponseManager.handle(
            request.data, dispatcher)
        return Response(response.json, mimetype='application/json')


    if __name__ == '__main__':
        run_simple('localhost', 4000, application)

Client (uses [requests](http://www.python-requests.org/en/latest/))

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
        assert response["jsonrpc"]
        assert response["id"] == 0

    if __name__ == "__main__":
        main()

Competitors
-----------
There are [several libraries](http://en.wikipedia.org/wiki/JSON-RPC#Implementations) implementing JSON-RPC protocol. List below represents python libraries, none of the supports python3. tinyrpc looks better than others.

| # |package         | version                                                                                                 | last modified |
|---|----------------|---------------------------------------------------------------------------------------------------------|---------------|
| 1 |python-jsonrpc  | [![Downloads](https://pypip.in/v/python-jsonrpc/badge.png)](https://crate.io/packages/python-jsonrpc)   | 2013-07-07    |
| 2 |jsonrpc         | [![Downloads](https://pypip.in/v/jsonrpc/badge.png)](https://crate.io/packages/jsonrpc)                 | 2012-02-06    |
| 3 |jsonrpc2        | [![Downloads](https://pypip.in/v/jsonrpc2/badge.png)](https://crate.io/packages/jsonrpc2)               | 2011-06-06    |
| 4 |tinyrpc         | [![Downloads](https://pypip.in/v/tinyrpc/badge.png)](https://crate.io/packages/tinyrpc)                 | 2013-02-24    |
| 5 |simple-json-rpc | [![Downloads](https://pypip.in/v/simple-json-rpc/badge.png)](https://crate.io/packages/simple-json-rpc) | 2012-06-16    |
| 6 |pjsonrpc        | -                                                                                                       | 2011          |
