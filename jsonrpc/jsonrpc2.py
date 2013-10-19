from . import six
import json

from .exceptions import JSONRPCError
from .jsonrpc import JSONRPCBaseRequest

JSONRPC_VERSION = "2.0"


class JSONRPC20Request(JSONRPCBaseRequest):

    """ A rpc call is represented by sending a Request object to a Server.

    :param str method: A String containing the name of the method to be
        invoked. Method names that begin with the word rpc followed by a
        period character (U+002E or ASCII 46) are reserved for rpc-internal
        methods and extensions and MUST NOT be used for anything else.

    :param params: A Structured value that holds the parameter values to be
        used during the invocation of the method. This member MAY be omitted.
    :type params: iterable or dict

    :param _id: An identifier established by the Client that MUST contain a
        String, Number, or NULL value if included. If it is not included it is
        assumed to be a notification. The value SHOULD normally not be Null
        [1] and Numbers SHOULD NOT contain fractional parts [2].
    :type _id: str or int or None

    :param bool is_notification: Whether request is notification or not. If
        value is True, _id is not included to request. It allows to create
        requests with id = null.

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

    @property
    def data(self):
        data = {
            k: v for k, v in self._data.items()
            if not (k == "id" and self.is_notification)
        }
        data["jsonrpc"] = JSONRPC_VERSION
        return data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError("data should be dict")

        self._data = value

    @property
    def method(self):
        return self._data.get("method")

    @method.setter
    def method(self, value):
        if not isinstance(value, six.string_types):
            raise ValueError("Method should be string")

        if value.startswith("rpc."):
            raise ValueError(
                "Method names that begin with the word rpc followed by a " +
                "period character (U+002E or ASCII 46) are reserved for " +
                "rpc-internal methods and extensions and MUST NOT be used " +
                "for anything else.")

        self._data["method"] = str(value)

    @property
    def params(self):
        return self._data.get("params")

    @params.setter
    def params(self, value):
        if value is not None and not isinstance(value, (list, tuple, dict)):
            raise ValueError("Incorrect params {}".format(value))

        value = list(value) if isinstance(value, tuple) else value

        if value is not None:
            self._data["params"] = value

    @property
    def _id(self):
        return self._data.get("id")

    @_id.setter
    def _id(self, value):
        if value is not None and \
           not isinstance(value, six.string_types + six.integer_types):
            raise ValueError("id should be string or integer")

        self._data["id"] = value

    @classmethod
    def from_json(cls, json_str):
        data = cls.deserialize(json_str)

        is_batch = isinstance(data, list)
        data = data if is_batch else [data]

        if not data:
            raise ValueError("[] value is not accepted")

        if not all(isinstance(d, dict) for d in data):
            raise ValueError("Each request should be an object (dict)")

        try:
            result = [JSONRPC20Request(
                method=d["method"], params=d.get("params"), _id=d.get("id"),
                is_notification="id" not in d,
            ) for d in data]
        except KeyError as e:
            raise ValueError("Incorrect Request {}".format(str(e)))

        return result if len(result) > 1 or is_batch else result[0]


class JSONRPC20BatchRequest(object):

    """ Batch JSON-RPC 2.0 Request.

    :param JSONRPC20Request *requests: requests

    """

    def __init__(self, *requests):
        self.requests = requests

    @classmethod
    def from_json(cls, json_str):
        return JSONRPC20Request.from_json(json_str)

    @property
    def json(self):
        return json.dumps([r.data for r in self.requests])

    def __iter__(self):
        return iter(self.requests)


class JSONRPC20Response(object):

    """ JSON-RPC response object to JSONRPC20Request.

    When a rpc call is made, the Server MUST reply with a Response, except for
    in the case of Notifications. The Response is expressed as a single JSON
    Object, with the following members:

    :param str jsonrpc: A String specifying the version of the JSON-RPC
        protocol. MUST be exactly "2.0".

    :param result: This member is REQUIRED on success.
        This member MUST NOT exist if there was an error invoking the method.
        The value of this member is determined by the method invoked on the
        Server.

    :param dict error: This member is REQUIRED on error.
        This member MUST NOT exist if there was no error triggered during
        invocation. The value for this member MUST be an Object.

    :param id: This member is REQUIRED.
        It MUST be the same as the value of the id member in the Request
        Object. If there was an error in detecting the id in the Request
        object (e.g. Parse error/Invalid Request), it MUST be Null.
    :type id: str or int or None

    Either the result member or error member MUST be included, but both
    members MUST NOT be included.

    """

    serialize = staticmethod(json.dumps)

    def __init__(self, result=None, error=None, _id=None):
        self.data = dict(jsonrpc=self.jsonrpc)

        if result is None and error is None:
            raise ValueError("Either result or error should be used")

        self.result = result
        self.error = error
        self._id = _id

    @property
    def jsonrpc(self):
        return JSONRPC_VERSION

    def __get_result(self):
        return self.data.get("result")

    def __set_result(self, value):
        if value is not None:
            if self.error is not None:
                raise ValueError("Either result or error should be used")

            self.data["result"] = value

    result = property(__get_result, __set_result)

    def __get_error(self):
        return self.data.get("error")

    def __set_error(self, value):
        if value is not None:
            if self.result is not None:
                raise ValueError("Either result or error should be used")

            JSONRPCError(**value)
            self.data["error"] = value

    error = property(__get_error, __set_error)

    def __get_id(self):
        return self.data["_id"]

    def __set_id(self, value):
        if value is not None and \
           not isinstance(value, six.string_types + six.integer_types):
            raise ValueError("id should be string or integer")

        self.data["id"] = value

    _id = property(__get_id, __set_id)

    @property
    def json(self):
        return self.serialize(self.data)


class JSONRPC20BatchResponse(object):
    def __init__(self, *responses):
        self.responses = responses

    @property
    def data(self):
        return [r.data for r in self.responses]

    @property
    def json(self):
        return json.dumps(self.data)

    def __iter__(self):
        return iter(self.responses)
