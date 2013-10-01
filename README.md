json-rpc
========

[![Downloads](https://pypip.in/v/json-rpc/badge.png)](https://crate.io/packages/json-rpc)
[![Downloads](https://pypip.in/d/json-rpc/badge.png)](https://crate.io/packages/json-rpc)

JSON-RPC2.0 transport with python3 support. Implementation follows [JSON-RPC](http://www.jsonrpc.org/specification) specification.


Overview
--------

JSON-RPC is a stateless, light-weight remote procedure call (RPC) protocol. Primarily this specification defines several data structures and the rules around their processing. It is transport agnostic in that the concepts can be used within the same process, over sockets, over http, or in many various message passing environments. It uses JSON (RFC 4627) as data format.

It is designed to be simple!

Install
-------

    pip install json-rpc

Tests
-----

All of the tests requirements are in ``setup.py`` file.

    python setup.py test
    
Competitors
-----------
There are [several libraries](http://en.wikipedia.org/wiki/JSON-RPC#Implementations) implementing JSON-RPC protocol. List below represents python libraries, none of the supports python3. tinyrpc looks better than others.

| # |package         | version | last modified | doc | source |
|---|----------------|---------|---------------|-----|--------|
| 1 |python-jsonrpc  | 0.3.4   | 2013-07-07    |
| 2 |jsonrpc         | 1.2     | 2012-02-06    |
| 3 |jsonrpc2        | 0.3.2   | 2011-06-06    |
| 4 |tinyrpc         | 0.5     | 2013-02-24    |
| 5 |simple-json-rpc | 0.3.4   | 2012-06-16    |
| 6 |pjsonrpc        | -       | 2011          |
