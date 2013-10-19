from . import six
import json

from .jsonrpc import JSONRPCBaseRequest

JSONRPC_VERSION = "1.0"


class JSONRPC10Request(JSONRPCBaseRequest):

    """ JSON-RPC 1.0 Request.

    A remote method is invoked by sending a request to a remote service.
    The request is a single object serialized using json.

    :param str method: The name of the method to be invoked.
    :param list params: An Array of objects to pass as arguments to the method.
    :param _id: This can be of any type. It is used to match the response with
        the request that it is replying to.
    :param bool is_notification: whether request notification or not.

    """

    @property
    def data(self):
        data = self._data.items()
        data["id"] = None if self.is_notification else data["id"]
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

        self._data["method"] = str(value)

    @property
    def params(self):
        return self._data.get("params")

    @params.setter
    def params(self, value):
        if not isinstance(value, (list, tuple)):
            raise ValueError("Incorrect params {}".format(value))

        self._data["params"] = list(value)

    @property
    def _id(self):
        return self._data.get("id")

    @_id.setter
    def _id(self, value):
        self._data["id"] = value

    @property
    def is_notifiation(self):
        return self._data["id"] is None or self._is_notification

    @is_notifiation.setter
    def is_notifiation(self, value):
        if not value and self._data["id"] is None:
            raise ValueError("Can not set attribute is_notification. " +
                             "Request is should not be None")

        self._is_notification = value


class JSONRPC10Response(object):
    pass
