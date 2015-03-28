Quickstart
==========

Installation
------------

.. highlight:: bash

:Requirements: **Python 2.6, 2.7**, **Python 3.x >= 3.2** or **PyPy**

To install the latest released version of package::

    pip install json-rpc

Integration
-----------

Package is transport agnostic, integration depends on you framework. As an example we have server with `Werkzeug <http://werkzeug.pocoo.org/>`_ and client with `requests <http://www.python-requests.org/en/latest/>`_.

Server

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

Client

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

Package ensures that request and response messages have correct format.
Besides that it provides :class:`jsonrpc.manager.JSONRPCResponseManager` which handles server common cases, such as incorrect message format or invalid method parameters.
Futher topics describe how to add methods to manager, how to handle custom exceptions and optional Django integration.
