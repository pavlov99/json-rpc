json-rpc
========

.. image:: https://travis-ci.org/pavlov99/json-rpc.png
    :target: https://travis-ci.org/pavlov99/json-rpc
    :alt: Build Status

.. image:: https://coveralls.io/repos/pavlov99/json-rpc/badge.png
    :target: https://coveralls.io/r/pavlov99/json-rpc
    :alt: Coverage Status

.. image:: https://pypip.in/v/json-rpc/badge.png
    :target: https://crate.io/packages/json-rpc
    :alt: Version

.. image:: https://pypip.in/d/json-rpc/badge.png
    :target: https://crate.io/packages/json-rpc
    :alt: Downloads

.. image:: https://pypip.in/format/json-rpc/badge.png
    :target: https://pypi.python.org/pypi/json-rpc/
    :alt: Download format


.. image:: https://pypip.in/license/json-rpc/badge.png
    :target: https://pypi.python.org/pypi/json-rpc/
    :alt: License


`JSON-RPC2.0 <http://www.jsonrpc.org/specification>`_ and `JSON-RPC1.0 <http://json-rpc.org/wiki/specification>`_ transport specification implementation. Supports python2.6+, python3.2+.

Documentation: http://json-rpc.readthedocs.org

This implementation does not have any transport functionality realization, only protocol.
Any client or server realization is easy based on current code, but requires transport libraries, such as requests, gevent or zmq, see `examples <https://github.com/pavlov99/json-rpc/tree/master/examples>`_.

Install
-------

.. code-block:: python

    pip install json-rpc

Tests
-----

.. code-block:: python

    tox

Quickstart
----------
Server (uses `Werkzeug <http://werkzeug.pocoo.org/>`_)

.. code-block:: python

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

Client (uses `requests <http://www.python-requests.org/en/latest/>`_)

.. code-block:: python

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
There are `several libraries <http://en.wikipedia.org/wiki/JSON-RPC#Implementations>`_ implementing JSON-RPC protocol. List below represents python libraries, none of the supports python3. tinyrpc looks better than others.
