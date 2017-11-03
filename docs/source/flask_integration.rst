Integration with Flask
======================

.. note:: Flask backend is optionaly supported. Library itself does not depend on Flask.

Create api instance
-------------------

If you want to use default (global) object, skip this step. In most cases it is enough to start with it, even if you plan to add another version later. Default api is located here:

.. code-block:: python

   from jsonrpc.backend.flask import api


If you would like to use different api versions (not, you could name methods differently) or use custom dispatcher, use

.. code-block:: python

   from jsonrpc.backend.flask import JSONRPCAPI
   api = JSONRPCAPI(dispatcher=<my_dispatcher>)

Later on we assume that you use default api instance.

Add api endpoint to the project
-------------------------------

You have to options to add new endpoint to your Flask application.

First - register as a blueprint. In this case, as small bonus, you got a /map handler, which prints all registered methods.

.. code-block:: python

    from flask import Flask

    from jsonrpc.backend.flask import api

    app = Flask(__name__)
    app.register_blueprint(api.as_blueprint())


Second - register as a usual view.

.. code-block:: python

    from flask import Flask

    from jsonrpc.backend.flask import api

    app = Flask(__name__)
    app.add_url_rule('/', 'api', api.as_view(), methods=['POST'])


Add methods to api
------------------

.. code-block:: python

    @api.dispatcher.add_method
    def my_method(*args, **kwargs):
        return args, kwargs


Make requests to api
--------------------

To use api, send `POST` request to api address. Make sure your message has correct format.
