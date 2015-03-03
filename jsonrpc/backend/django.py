from __future__ import absolute_import

from django.conf.urls import url
from django.http import HttpResponse, HttpResponseNotAllowed
import json

from ..exceptions import JSONRPCInvalidRequestException
from ..jsonrpc import JSONRPCRequest
from ..manager import JSONRPCResponseManager
from ..utils import DatetimeDecimalEncoder
from ..dispatcher import Dispatcher


class JSONRPCAPI(object):
    def __init__(self, dispatcher=None):
        self.dispatcher = dispatcher or Dispatcher()

    @property
    def urls(self):
        urls = [
            url(r'^$', self.jsonrpc),
            url(r'^map$', self.jsonrpc_map),
        ]

        return urls

    def jsonrpc(self, request):
        """ JSON-RPC 2.0 handler."""
        if request.method != "POST":
            return HttpResponseNotAllowed(["POST"])

        request_str = request.body.decode('utf8')
        try:
            jsonrpc_request = JSONRPCRequest.from_json(request_str)
        except (TypeError, ValueError, JSONRPCInvalidRequestException):
            response = JSONRPCResponseManager.handle(
                request_str, self.dispatcher)
        else:
            jsonrpc_request.params = jsonrpc_request.params or {}
            if isinstance(jsonrpc_request.params, dict):
                jsonrpc_request.params.update(request=request)
            response = JSONRPCResponseManager.handle_request(
                jsonrpc_request, self.dispatcher)

        if response:
            def serialize(s):
                return json.dumps(s, cls=DatetimeDecimalEncoder)

            response.serialize = serialize
            response = response.json

        return HttpResponse(response, content_type="application/json")

    def jsonrpc_map(self, request):
        """ Map of json-rpc available calls.

        :return str:

        """
        result = "<h1>JSON-RPC map</h1><pre>{}</pre>".format("\n\n".join([
            "{}: {}".format(fname, f.__doc__)
            for fname, f in self.dispatcher.items()
        ]))
        return HttpResponse(result)


api = JSONRPCAPI()
