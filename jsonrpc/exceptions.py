class JSONRPCError(object):

    """ Error for JSON-RPC communication.

    When a rpc call encounters an error, the Response Object MUST contain the
    error member with a value that is a Object with the following members:

    code: A Number that indicates the error type that occurred.
        This MUST be an integer.

    message: A String providing a short description of the error.
        The message SHOULD be limited to a concise single sentence.

    data: A Primitive or Structured value that contains additional information
        about the error.
        This may be omitted.
        The value of this member is defined by the Server (e.g. detailed error
        information, nested errors etc.).

    The error codes from and including -32768 to -32000 are reserved for
    pre-defined errors. Any code within this range, but not defined explicitly
    below is reserved for future use. The error codes are nearly the same as
    those suggested for XML-RPC at the following
    url: http://xmlrpc-epi.sourceforge.net/specs/rfc.fault_codes.php

    """

    def __init__(self, code=None, message=None, data=None):
        self.code = code or self.code
        self.message = message or self.message
        self.data = data

    @property
    def _dict(self):
        """ Return object dict representation.

        :return dict:

        """
        data = dict(code=self.code, message=self.message)

        if self.data:
            data["data"] = self.data

        return data


class JSONRPCParseError(JSONRPCError):

    """ Parse Error.

    Invalid JSON was received by the server.
    An error occurred on the server while parsing the JSON text.

    """

    code = -32700
    message = "Parse error"


class JSONRPCInvalidRequest(JSONRPCError):

    """ Invalid Request.

    The JSON sent is not a valid Request object.

    """

    code = -32600
    message = "Invalid Request"


class JSONRPCMethodNotFound(JSONRPCError):

    """ Method not found.

    The method does not exist / is not available.

    """

    code = -32601
    message = "Method not found"


class JSONRPCInvalidParams(JSONRPCError):

    """ Invalid params.

    Invalid method parameter(s).

    """

    code = -32602
    message = "Invalid params"


class JSONRPCInternalError(JSONRPCError):

    """ Internal error.

    Internal JSON-RPC error.

    """

    code = -32603
    message = "Internal error"


class JSONRPCServerError(JSONRPCError):

    """ Server error.

    Reserved for implementation-defined server-errors.

    """

    code = -32000
    message = "Server error"
