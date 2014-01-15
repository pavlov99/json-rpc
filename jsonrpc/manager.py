import json
from .exceptions import (
    JSONRPCInvalidParams,
    JSONRPCInvalidRequest,
    JSONRPCInvalidRequestException,
    JSONRPCMethodNotFound,
    JSONRPCParseError,
    JSONRPCServerError,
)
from .jsonrpc1 import JSONRPC10Response
from .jsonrpc2 import (
    JSONRPC20BatchRequest,
    JSONRPC20BatchResponse,
    JSONRPC20Response,
)
from .jsonrpc import JSONRPCRequest


class JSONRPCResponseManager(object):

    """ JSON-RPC response manager.

    Method brings syntactic sugar into library. Given dispatcher it handles
    request (both single and batch) and handles errors.
    Request could be handled in parallel, it is server responsibility.

    :param str request_str: json string. Will be converted into
        JSONRPC20Request, JSONRPC20BatchRequest or JSONRPC10Request

    :param dict dispather: dict<function_name:function>.

    """

    RESPONSE_CLASS_MAP = {
        "1.0": JSONRPC10Response,
        "2.0": JSONRPC20Response,
    }

    @classmethod
    def handle(cls, request_str, dispatcher):
        if isinstance(request_str, bytes):
            request_str = request_str.decode("utf-8")

        try:
            json.loads(request_str)
        except (TypeError, ValueError):
            return JSONRPC20Response(error=JSONRPCParseError()._data)

        try:
            request = JSONRPCRequest.from_json(request_str)
        except JSONRPCInvalidRequestException:
            return JSONRPC20Response(error=JSONRPCInvalidRequest()._data)

        rs = request if isinstance(request, JSONRPC20BatchRequest) \
            else [request]
        responses = [r for r in cls._get_responses(rs, dispatcher)
                     if r is not None]

        # notifications
        if not responses:
            return

        if isinstance(request, JSONRPC20BatchRequest):
            return JSONRPC20BatchResponse(*responses)
        else:
            return responses[0]

    @classmethod
    def _get_responses(cls, requests, dispatcher):
        """ Response to each single JSON-RPC Request.

        :return iterator(JSONRPC20Response):

        """
        for request in requests:
            response = lambda **kwargs: cls.RESPONSE_CLASS_MAP[
                request.JSONRPC_VERSION](_id=request._id, **kwargs)

            if request.is_notification:
                yield
                continue

            try:
                method = dispatcher[request.method]
            except KeyError:
                yield response(error=JSONRPCMethodNotFound()._data)
                continue

            try:
                result = method(*request.args, **request.kwargs)
            except TypeError:
                #import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
                yield response(error=JSONRPCInvalidParams()._data)
                continue
            except Exception as e:
                data = {
                    "type": e.__class__.__name__,
                    "args": e.args,
                    "message": str(e),
                }
                yield response(error=JSONRPCServerError(data=data)._data)
                continue

            yield response(result=result)
