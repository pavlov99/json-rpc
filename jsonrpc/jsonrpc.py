#import json
#from . import six
#from .exceptions import (
    #JSONRPCError,
    #JSONRPCInvalidParams,
    #JSONRPCInvalidRequest,
    #JSONRPCMethodNotFound,
    #JSONRPCParseError,
    #JSONRPCServerError,
#)
from .utils import JSONSerializable


class JSONRPCBaseRequest(JSONSerializable):

    """ Base class for JSON-RPC 1.0 and JSON-RPC 2.0 requests. """

    def __init__(self, method=None, params=None, _id=None,
                 is_notification=None):
        self.data = dict()
        self.method = method
        self.params = params
        self._id = _id
        self.is_notification = is_notification

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError("data should be dict")

        self._data = value

    @property
    def args(self):
        """ Method position arguments.

        :return tuple args: method position arguments.

        """
        return tuple(self.params) if isinstance(self.params, list) else ()

    @property
    def kwargs(self):
        """ Method named arguments.

        :return dict kwargs: method named arguments.

        """
        return self.params if isinstance(self.params, dict) else {}

    @property
    def json(self):
        return self.serialize(self.data)

    @classmethod
    def from_json(cls, json_str):
        data = cls.deserialize(json_str)

        if not isinstance(data, dict):
            raise ValueError("data should be dict")

        return cls(**data)


#class JSONRPC20ResponseManager(object):

    #""" JSON-RPC response manager.

    #Method brings syntactic sugar into library. Given dispatcher it handles
    #request (both single and batch) and handles errors.
    #Request could be handled in parallel, it is server responsibility.

    #:param str request_str: json string. Will be converted into
        #JSONRPC20Request or JSONRPC20BatchRequest

    #:param dict dispather: dict<function_name:function>.

    #"""

    #@classmethod
    #def handle(cls, request_str, dispatcher):
        #try:
            #json.loads(request_str)
        #except (TypeError, ValueError):
            #return JSONRPC20Response(error=JSONRPCParseError().data)

        #try:
            #request = JSONRPC20Request.from_json(request_str)
        #except ValueError:
            #return JSONRPC20Response(error=JSONRPCInvalidRequest().data)

        #rs = [request] if isinstance(request, JSONRPC20Request) else request
        #responses = [r for r in cls._get_responses(rs, dispatcher)
                     #if r is not None]

        ## notifications
        #if not responses:
            #return

        #if isinstance(request, JSONRPC20Request):
            #return responses[0]
        #else:
            #return JSONRPC20BatchResponse(*responses)

    #@classmethod
    #def _get_responses(cls, requests, dispatcher):
        #""" Response to each single JSON-RPC Request.

        #:return iterator(JSONRPC20Response):

        #"""
        #for request in requests:
            #response = lambda **kwargs: JSONRPC20Response(
                #_id=request._id, **kwargs)

            #if request.is_notification:
                #yield
                #continue

            #try:
                #method = dispatcher[request.method]
            #except KeyError:
                #yield response(error=JSONRPCMethodNotFound().data)
                #continue

            #try:
                #result = method(*request.args, **request.kwargs)
            #except TypeError:
                #yield response(error=JSONRPCInvalidParams().data)
                #continue
            #except Exception as e:
                #data = {
                    #"type": e.__class__.__name__,
                    #"args": e.args,
                    #"message": str(e),
                #}
                #yield response(error=JSONRPCServerError(data=data).data)
                #continue

            #yield response(result=result)
