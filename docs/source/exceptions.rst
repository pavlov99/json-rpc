Exceptions
==========

According to specification, error code should be in response message. Http
server should respond with status code 200, even if there is an error.

JSON-RPC Error messages
-----------------------

Error messages are members of :class:`~jsonrpc.exceptions.JSONRPCError` class. Any custom error messages should be inherited from it.

JSON-RPC has several predefined errors, each of them has reserver error code which should not be used for custom exceptions.

JSON-RPC Custom exceptions
--------------------------
a
