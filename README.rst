json-rpc
========

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/pavlov99/json-rpc
   :target: https://gitter.im/pavlov99/json-rpc?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://travis-ci.org/pavlov99/json-rpc.png?branch=master
    :target: https://travis-ci.org/pavlov99/json-rpc?branch=master
    :alt: Build Status

.. image:: https://coveralls.io/repos/pavlov99/json-rpc/badge.png?branch=master
    :target: https://coveralls.io/r/pavlov99/json-rpc?branch=master
    :alt: Coverage Status
    
.. image:: https://www.codacy.com/project/badge/34e0c2c696214041ae4fd5cfcb4af401
    :target: https://www.codacy.com/app/pavlov99/json-rpc


`JSON-RPC2.0 <http://www.jsonrpc.org/specification>`_ and `JSON-RPC1.0 <http://json-rpc.org/wiki/specification>`_ transport specification implementation.
Supports python2.6+, python3.3+, PyPy. Has optional Django and Flask support. 200+ tests.

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

Features
--------

- Vanilla python, no dependencies
- Optional backend support for Django, Flask
- json-rpc 1.1 and 2.0 support

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


Testing
-------
json-rpc is a python library, it supports pythons: 2.6, 2.7, 3.3, 3.4. There is optional support for django1.6 (python2.6 does not support django1.7).

Contributors
------------

* Kirill Pavlov `@pavlov99 <https://github.com/pavlov99>`_
* Jan Willems `@jw <https://github.com/jw>`_
* Robby Dermody (xnova) `@robby-dermody <https://github.com/robby-dermody>`_
* matee911 `@matee911 <https://github.com/matee911>`_
* Malyshev Artem `@proofit404 <https://github.com/proofit404>`_
* Julian Hille `@julianhille <https://github.com/julianhille>`_
* Pavel Evdokimov `@Santinell <https://github.com/Santinell>`_
* Lev Orekhov `@lorehov <https://github.com/lorehov>`_
* Sergey Nikitin `@nikitinsm <https://github.com/nikitinsm>`_
* Jean-Christophe Bohin `@jcbohin <https://github.com/jcbohin>`_
* arnuschky `@arnuschky <https://github.com/arnuschky>`_
