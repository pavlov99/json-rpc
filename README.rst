json-rpc
========

.. image:: https://github.com/pavlov99/json-rpc/actions/workflows/tests.yml/badge.svg?branch=master
    :target: https://github.com/pavlov99/json-rpc/actions/workflows/tests.yml
    :alt: Build Status

.. image:: https://codecov.io/gh/pavlov99/json-rpc/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/pavlov99/json-rpc
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/json-rpc/badge/?version=latest
    :target: http://json-rpc.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/v/json-rpc.svg
    :target: https://pypi.org/project/json-rpc/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/json-rpc.svg
    :target: https://pypi.org/project/json-rpc/
    :alt: Supported Python versions

.. image:: https://opencollective.com/json-rpc/tiers/backer/badge.svg?label=backer&color=brightgreen
    :target: https://opencollective.com/json-rpc
    :alt: Bakers

.. image:: https://opencollective.com/json-rpc/tiers/backer/badge.svg?label=sponsor&color=brightgreen
    :target: https://opencollective.com/json-rpc
    :alt: Sponsors

.. important::

   **json-rpc 2.0 is being planned.** After more than a decade of stable releases, json-rpc is being modernized:

   - **Python ≥ 3.10**, type hints, no vendored ``six``
   - **Native asyncio** support, sharing one protocol core with the sync server
   - **Pluggable serialization** (``json``, ``orjson``, CBOR, ...) and error hooks
   - **Safer defaults**: responses are always valid JSON-RPC, and internal exception details are no longer sent to clients
   - Stricter spec compliance (batches, ids, JSON-RPC 1.0 responses) and new adapters for Starlette/FastAPI and aiohttp

   Existing code will keep working: ``JSONRPCResponseManager``, ``Dispatcher`` and the Django/Flask backends remain available through a compatibility layer.
   **1.15.x** remains the release line for Python 2.7 and Python 3 < 3.10 and will receive bug fixes.

   Roadmap, progress and ways to help: `#155 Roadmap: json-rpc 2.0 modernization <https://github.com/pavlov99/json-rpc/issues/155>`_.
   Feedback is very welcome.

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
Tests are an essential part of the library, as there are a lot of edge cases in the JSON-RPC standard. Run them with pytest; Django and Flask backend tests are skipped if those frameworks are not installed:

.. code-block:: bash

    pip install pytest django flask
    make test

The full matrix of Python versions runs in CI only; locally, testing with a single interpreter is enough.

Continuous integration
^^^^^^^^^^^^^^^^^^^^^^
This project uses `GitHub Actions <https://github.com/pavlov99/json-rpc/actions/workflows/tests.yml>`_ for continuous integration, configured in `.github/workflows/tests.yml`. Every push to master and every pull request is tested on CPython 2.7 and 3.6–3.14, PyPy 2.7 and PyPy 3, each in its official Docker image. A separate job builds the sdist and wheel, validates them with `twine check`, and runs the test suite against the installed wheel.

Each job installs the newest pytest, Django and Flask releases that still support that interpreter, so cross-Django and cross-Flask support follows what each Python version can run. The exact versions are printed in the "Show versions" step of every job.

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

        # Example echo method
        payload = {
            "method": "echo",
            "params": ["echome!"],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(url, json=payload).json()

        assert response["result"] == "echome!"
        assert response["jsonrpc"]
        assert response["id"] == 0

    if __name__ == "__main__":
        main()

Competitors
-----------
There are `several libraries <http://en.wikipedia.org/wiki/JSON-RPC#Implementations>`_ implementing JSON-RPC protocol. List below represents python libraries, none of the supports python3. tinyrpc looks better than others.
