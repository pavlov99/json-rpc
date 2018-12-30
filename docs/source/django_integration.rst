Integration with Django
=======================

.. note:: Django backend is optionally supported. Library itself does not depend on Django.

Django integration is similar project to project. Starting from version 1.8.4 json-rpc support it and provides convenient way of integration. To add json-rpc to Django project follow steps.

Create api instance
-------------------

If you want to use default (global) object, skip this step. In most cases it is enougth to start with it, even if you plan to add another version later. Default api is located here:

.. code-block:: python

   from jsonrpc.backend.django import api


If you would like to use different api versions (not, you could name methods differently) or use cudtom dispatcher, use

.. code-block:: python

   from jsonrpc.backend.django import JSONRPCAPI
   api = JSONRPCAPI(dispatcher=<my_dispatcher>)

Later on we assume that you use default api instance

Add api urls to the project
---------------------------

In your urls.py file add

.. code-block:: python

    urlpatterns = patterns(
        ...
        url(r'^api/jsonrpc/', include(api.urls)),
    )

Add methods to api
------------------

.. code-block:: python

    @api.dispatcher.add_method
    def my_method(request, *args, **kwargs):
        return args, kwargs

.. note:: first argument of each method should be request. In this case it is possible to get user and control access to data

Make requests to api
--------------------

To use api, send `POST` request to api address. Make sure your message has correct format.
Also json-rpc generates method's map. It is available at `<api_url>/map` url.
