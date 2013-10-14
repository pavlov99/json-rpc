""" Example of json-rpc usage with Wergzeug and requests.

NOTE: there are no Werkzeug and requests in dependencies of json-rpc.
NOTE: server handles all url paths the same way (there are no different urls).

"""

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc.jsonrpc import JSONRPCResponseManager


@Request.application
def application(request):
    # Dispatcher is a dictionary {<method_name>: callable function}
    dispatcher = {
        "echo": lambda s: s,
        "add": lambda a, b: a + b,
        "foobar": lambda **kwargs: kwargs["foo"] + kwargs["bar"],
    }

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
