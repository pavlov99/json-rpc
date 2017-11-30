import json
import logging
import time

from .utils import is_invalid_params
from .exceptions import (
    JSONRPCInvalidParams,
    JSONRPCInvalidRequest,
    JSONRPCInvalidRequestException,
    JSONRPCMethodNotFound,
    JSONRPCParseError,
    JSONRPCServerError,
    JSONRPCDispatchException,
)
from .jsonrpc1 import JSONRPC10Response
from .jsonrpc2 import (
    JSONRPC20BatchRequest,
    JSONRPC20BatchResponse,
    JSONRPC20Response,
)
from .jsonrpc import JSONRPCRequest

logger = logging.getLogger(__name__)


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
            data = json.loads(request_str)
        except (TypeError, ValueError):
            return JSONRPC20Response(error=JSONRPCParseError()._data)

        try:
            request = JSONRPCRequest.from_data(data)
        except JSONRPCInvalidRequestException:
            return JSONRPC20Response(error=JSONRPCInvalidRequest()._data)

        return cls.handle_request(request, dispatcher)

    @classmethod
    def handle_request(cls, request, dispatcher):
        """ Handle request data.

        At this moment request has correct jsonrpc format.

        :param dict request: data parsed from request_str.
        :param jsonrpc.dispatcher.Dispatcher dispatcher:

        .. versionadded: 1.8.0

        """
        if isinstance(request, JSONRPC20BatchRequest):
            rs = request
        else:
            rs = [request]

        for r in rs:
            r.params = r.params or {}
            if isinstance(r.params, dict):
                r.params.update(request=r)

        responses = []

        t1 = time.time()

        for response in cls._get_responses(rs, dispatcher):
            if response is not None:
                logger.info('executed {0}({1})'.format(
                    response.request.method,
                    response.request.params
                ))

                responses.append(response)

        t2 = time.time()

        logger.info('executed {0} in {1:.1f} sec'.format(
            ['{0}({1})'.format(r.method, r.params) for r in rs],
            t2 - t1
        ))

        # notifications
        if not responses:
            return

        if isinstance(request, JSONRPC20BatchRequest):
            response = JSONRPC20BatchResponse(*responses)
            response.request = request
            return response
        else:
            return responses[0]

    @classmethod
    def _get_responses(cls, requests, dispatcher):
        """ Response to each single JSON-RPC Request.

        :return iterator(JSONRPC20Response):

        .. versionadded: 1.9.0
          TypeError inside the function is distinguished from Invalid Params.

        """
        for request in requests:
            def make_response(**kwargs):
                response = cls.RESPONSE_CLASS_MAP[request.JSONRPC_VERSION](
                    _id=request._id, **kwargs)
                response.request = request
                return response

            try:
                method = dispatcher[request.method]
            except KeyError:
                output = make_response(error=JSONRPCMethodNotFound()._data)
            else:
                try:
                    result = method(*request.args, **request.kwargs)
                except JSONRPCDispatchException as e:
                    output = make_response(error=e.error._data)
                except Exception as e:
                    data = {
                        "type": e.__class__.__name__,
                        "args": e.args,
                        "message": str(e),
                    }

                    logger.exception("API Exception: {0}".format(data))

                    if isinstance(e, TypeError) and is_invalid_params(
                            method, *request.args, **request.kwargs):
                        output = make_response(
                            error=JSONRPCInvalidParams(data=data)._data)
                    else:
                        output = make_response(
                            error=JSONRPCServerError(data=data)._data)
                else:
                    output = make_response(result=result)
            finally:
                if not request.is_notification:
                    yield output
