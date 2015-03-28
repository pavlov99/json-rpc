.. json-rpc documentation master file, created by
   sphinx-quickstart on Sun Oct 13 15:41:10 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

JSON-RPC transport implementation
=================================

:Source code: https://github.com/pavlov99/json-rpc
:Issue tracker: https://github.com/pavlov99/json-rpc/issues


JSON-RPC is a stateless, light-weight remote procedure call (RPC) protocol. Primarily this specification defines several data structures and the rules around their processing. It is transport agnostic in that the concepts can be used within the same process, over sockets, over http, or in many various message passing environments. It uses JSON (RFC 4627) as data format.

Features
--------

* Supports `JSON-PRC2.0 <http://www.jsonrpc.org/specification>`_ and `JSON-RPC1.0 <http://json-rpc.org/wiki/specification>`_
* Implementation is complete and 100% tested
* Does not depend on transport realisation, no external dependencies
* It comes with request manager and optional Django support
* Compatible with Python 2.6, 2.7, 3.x >= 3.2, PyPy

Contents
--------

.. toctree::
    :maxdepth: 2

    quickstart
    dispatcher
    exceptions
    django_integration

    jsonrpc
