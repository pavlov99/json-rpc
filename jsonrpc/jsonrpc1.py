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
    pass


class JSONRPC10Response(object):
    pass
