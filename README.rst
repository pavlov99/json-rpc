json-rpc
========

.. image:: https://travis-ci.org/pavlov99/json-rpc.png?branch=master
    :target: https://travis-ci.org/pavlov99/json-rpc?branch=master
    :alt: Build Status

.. image:: https://coveralls.io/repos/pavlov99/json-rpc/badge.png?branch=master
    :target: https://coveralls.io/r/pavlov99/json-rpc?branch=master
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/json-rpc/badge/?version=latest
    :target: http://json-rpc.readthedocs.io/en/latest/?badge=latest

.. image:: https://www.codacy.com/project/badge/34e0c2c696214041ae4fd5cfcb4af401
    :target: https://www.codacy.com/app/pavlov99/json-rpc

.. image:: https://img.shields.io/pypi/v/json-rpc.svg
    :target: https://pypi.org/project/json-rpc/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/json-rpc.svg
    :target: https://pypi.org/project/json-rpc/
    :alt: Supported Python versions

.. image:: https://badges.gitter.im/pavlov99/json-rpc.svg
    :target: https://gitter.im/pavlov99/json-rpc
    :alt: Gitter

`JSON-RPC2.0 <http://www.jsonrpc.org/specification>`_ and `JSON-RPC1.0 <http://json-rpc.org/wiki/specification>`_ transport specification implementation.
Supports Python 2.6+, Python 3.3+, PyPy. Has optional Django and Flask support. 200+ tests.

Features
--------

This implementation does not have any transport functionality realization, only protocol.
Any client or server implementation is easy based on current code, but requires transport libraries, such as requests, gevent or zmq, see `examples <https://github.com/pavlov99/json-rpc/tree/master/examples>`_.

- Vanilla Python, no dependencies.
- 200+ tests for multiple edge cases.
- Optional backend support for Django, Flask.
- json-rpc 1.1 and 2.0 support.

Install
-------

.. code-block:: python

    pip install json-rpc

Tests
-----

Quickstart
^^^^^^^^^^
This is an essential part of the library as there are a lot of edge cases in JSON-RPC standard. To manage a variety of supported python versions as well as optional backends json-rpc uses `tox`:

.. code-block:: bash

    tox

.. TIP::
   During local development use your python version with tox runner. For example, if your are using Python 3.6 run `tox -e py36`. It is easier to develop functionality for specific version first and then expands it to all of the supported versions.

Continuous integration
^^^^^^^^^^^^^^^^^^^^^^
This project uses `Travis <https://travis-ci.org/>`_ for continuous integration. All of the python supported versions are managed via `tox.ini` and `.travis.yml` files. Only master and develop branches are tested. Master branch test status is displayed on the badge in the beginning of this document.

Test matrix
^^^^^^^^^^^
json-rpc supports multiple python versions: 2.6+, 3.3+, pypy. This introduces difficulties with testing libraries and optional dependencies management. For example, python before version 3.3 does not support `mock` and there is a limited support for `unittest2`. Every dependency translates into *if-then* blocks in the source code and adds complexity to it. Hence, while cross-python support is a core feature of this library, cross-Django or cross-Flask support is limited. In general, json-rpc uses latest stable release which supports current python version. For example, python 2.6 is compatible with Django 1.6 and not compatible with any future versions.

Below is a testing matrix:

+--------+-------+-------+-----------+--------+--------+
| Python | Tests | mock  | unittest  | Django | Flask  |
+========+=======+=======+===========+========+========+
| 2.6    | nose  | 2.0.0 | unittest2 | 1.6    | 0.12.2 |
+--------+-------+-------+-----------+--------+--------+
| 2.7    | nose2 | 2.0.0 |           | 1.11   | 0.12.2 |
+--------+-------+-------+-----------+--------+--------+
| 3.3    | nose2 |       |           | 1.11   | 0.12.2 |
+--------+-------+-------+-----------+--------+--------+
| 3.4    | nose2 |       |           | 1.11   | 0.12.2 |
+--------+-------+-------+-----------+--------+--------+
| 3.5    | nose2 |       |           | 1.11   | 0.12.2 |
+--------+-------+-------+-----------+--------+--------+
| 3.6    | nose2 |       |           | 1.11   | 0.12.2 |
+--------+-------+-------+-----------+--------+--------+
| pypy   | nose2 | 2.0.0 |           | 1.11   | 0.12.2 |
+--------+-------+-------+-----------+--------+--------+
| pypy3  | nose2 |       |           | 1.11   | 0.12.2 |
+--------+-------+-------+-----------+--------+--------+

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
