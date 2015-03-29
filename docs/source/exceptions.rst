Exceptions
==========

According to specification, error code should be in response message. Http
server should respond with status code 200, even if there is an error.

JSON-RPC Errors
---------------

.. note:: Error is an object which represent any kind of erros in JSON-RPC specification. It is not python Exception and could not be raised.

Errors (Error messages) are members of :class:`~jsonrpc.exceptions.JSONRPCError` class. Any custom error messages should be inherited from it.
The class is responsible for specification following and creates response string based on error's attributes.

JSON-RPC has several predefined errors, each of them has reserved code, which should not be used for custom errors.

+------------------+------------------+------------------------------------------------------------------------------------------------------+
| Code             | Message          | Meaning                                                                                              |
+------------------+------------------+------------------------------------------------------------------------------------------------------+
| -32700           | Parse error      | Invalid JSON was received by the server.An error occurred on the server while parsing the JSON text. |
+------------------+------------------+------------------------------------------------------------------------------------------------------+
| -32600           | Invalid Request  | The JSON sent is not a valid Request object.                                                         |
+------------------+------------------+------------------------------------------------------------------------------------------------------+
| -32601           | Method not found | The method does not exist / is not available.                                                        |
+------------------+------------------+------------------------------------------------------------------------------------------------------+
| -32602           | Invalid params   | Invalid method parameter(s).                                                                         |
+------------------+------------------+------------------------------------------------------------------------------------------------------+
| -32603           | Internal error   | Internal JSON-RPC error.                                                                             |
+------------------+------------------+------------------------------------------------------------------------------------------------------+
| -32000 to -32099 | Server error     | Reserved for implementation-defined server-errors.                                                   |
+------------------+------------------+------------------------------------------------------------------------------------------------------+

:class:`~jsonrpc.manager.JSONRPCResponseManager` handles common errors. If you do not plan to implement own manager, you do not need to write custom errors. To controll error messages and codes, json-rpc has exceptions, covered in next paragraph.

JSON-RPC Exceptions
-------------------

.. note:: Exception here a json-rpc library object and not related to specification. They are inherited from python Exception and could be raised.

JSON-RPC manager handles dispatcher method's exceptions, anything you raise would be catched.
There are two ways to generate error message in manager:

First is to simply raise exception in your method. Manager will catch it and return :class:`~jsonrpc.exceptions.JSONRPCServerError` message with description. Advantage of this mehtod is that everything is already implemented, just add method to dispatcher and manager will do the job.

If you need custom message code or error management, you might need to raise exception, inherited from :class:`~jsonrpc.exceptions.JSONRPCDispatchException`. Make sure, your exception class has error code.

.. versionadded:: 1.9.0
   Fix `Invalid params` error false generated if method raises TypeError. Now in this case manager introspects the code and returns proper exception.
