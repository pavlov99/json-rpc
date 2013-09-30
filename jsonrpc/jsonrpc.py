import json


class JSONRPCRequest(object):

    """ A rpc call is represented by sending a Request object to a Server.

    The Request object has the following members:

    jsonrpc: A String specifying the version of the JSON-RPC protocol. MUST be
        exactly "2.0".

    method: A String containing the name of the method to be invoked. Method
        names that begin with the word rpc followed by a period character
        (U+002E or ASCII 46) are reserved for rpc-internal methods and
        extensions and MUST NOT be used for anything else.

    params: A Structured value that holds the parameter values to be used
        during the invocation of the method. This member MAY be omitted.

    id: An identifier established by the Client that MUST contain a String,
        Number, or NULL value if included. If it is not included it is assumed
        to be a notification. The value SHOULD normally not be Null [1] and
        Numbers SHOULD NOT contain fractional parts [2].

    The Server MUST reply with the same value in the Response object if
    included. This member is used to correlate the context between the two
    objects.

    [1] The use of Null as a value for the id member in a Request object is
    discouraged, because this specification uses a value of Null for Responses
    with an unknown id. Also, because JSON-RPC 1.0 uses an id value of Null
    for Notifications this could cause confusion in handling.

    [2] Fractional parts may be problematic, since many decimal fractions
    cannot be represented exactly as binary fractions.

    """

    serialize = staticmethod(json.dumps)
    deserialize = staticmethod(json.loads)

    def __init__(self, method=None, params=None, _id=None):
        if not isinstance(method, str):
            raise ValueError("method should be string")

        assert isinstance(params, (list, dict))
        assert _id is None or isinstance(_id, (int, str))

        self.method = method
        self.params = params
        self.id = _id

    @property
    def json(self):
        data = dict(
            jsonrpc=JSONRPCProtocol.JSONRPC_VERSION,
            method=self.method,
            params=self.params,
        )

        if self.id:
            data["id"] = self.id

        return self.serialize(data)

    @classmethod
    def from_json(cls, json_str):
        return cls(**cls.deserializer(json_str))

    @property
    def is_notification(self):
        """ A Notification is a Request object without an "id" member.

        :return bool:

        """
        return self._id is None


class JSONRPCResponse(object):

    """ JSON-RPC response object to JSONRPCRequest.

    When a rpc call is made, the Server MUST reply with a Response, except for
    in the case of Notifications. The Response is expressed as a single JSON
    Object, with the following members:

    jsonrpc: A String specifying the version of the JSON-RPC protocol. MUST be
        exactly "2.0".

    result: This member is REQUIRED on success.
        This member MUST NOT exist if there was an error invoking the method.
        The value of this member is determined by the method invoked on the
        Server.

    error: This member is REQUIRED on error.
        This member MUST NOT exist if there was no error triggered during
        invocation. The value for this member MUST be an Object.

    id: This member is REQUIRED.
        It MUST be the same as the value of the id member in the Request
        Object. If there was an error in detecting the id in the Request
        object (e.g. Parse error/Invalid Request), it MUST be Null.

    Either the result member or error member MUST be included, but both
    members MUST NOT be included.

    """

    pass


class JSONRPCResponseError(object):

    """ JSON-RPC base error class.

    When a rpc call encounters an error, the Response Object MUST contain the
    error member with a value that is a Object with the following members:

    code: A Number that indicates the error type that occurred. This MUST be an
        integer.

    message: A String providing a short description of the error. The message
        SHOULD be limited to a concise single sentence.

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

    pass


class JSONRPCProtocol(object):

    """ JSON-RPC protocol implementation."""

    JSONRPC_VERSION = "2.0"

    @classmethod
    def create_request(cls, method, params, _id=None):
        return JSONRPCRequest(method, params, _id=_id)

    @classmethod
    def parse_request(cls, request):
        return JSONRPCRequest.from_json(request)
