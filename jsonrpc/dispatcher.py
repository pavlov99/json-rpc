""" Dispatcher is used to add methods (functions) to the server.

For usage examples see :meth:`Dispatcher.add_method`

"""
from . import six
import collections
from functools import wraps


class Dispatcher(collections.MutableMapping):

    """ Dictionary like object which maps method_name to method."""

    def __init__(self, prototype=None):
        """ Build method dispatcher.

        Parameters
        ----------
        prototype : object or dict, optional
            Initial method mapping.

        Examples
        --------

        Init object with method dictionary.

        >>> Dispatcher({"sum": lambda a, b: a + b})
        None

        """
        self._decorators = []
        self.method_map = dict()
        self._before_request_hooks = []
        self._error_handler_spec = {}

        if prototype is not None:
            self.build_method_map(prototype)

    def __getitem__(self, key):
        return self.method_map[key]

    def __setitem__(self, key, value):
        self.method_map[key] = self._wrap_method(value)

    def __delitem__(self, key):
        del self.method_map[key]

    def __len__(self):
        return len(self.method_map)

    def __iter__(self):
        return iter(self.method_map)

    def __repr__(self):
        return repr(self.method_map)

    def register_decorator(self, a):
        self._decorators.extend(a if hasattr(a, '__iter__') else [a])

    def before_request(self, hook):
        self._before_request_hooks.append(hook)

    def errorhandler(self, exception):
        def decorator(f):
            self._error_handler_spec[exception] = f
            return f
        return decorator

    def _wrap_method(self, f):
        @wraps(f)
        def _method(*args, **kwargs):
            for hook in self._before_request_hooks:
                hook()

            nf = f
            for deco in reversed(self._decorators):
                nf = deco(nf)

            try:
                return nf(*args, **kwargs)
            except Exception as e:
                for E, h in self._error_handler_spec.items():
                    if isinstance(e, E):
                        return h(e)
                raise

        return _method

    def add_class(self, cls):
        if hasattr(cls, 'rpc_method_prefix'):
            prefix = cls.rpc_method_prefix + '.'
        else:
            prefix = cls.__name__.lower() + '.'
        self.build_method_map(cls(), prefix)

        return cls  # for working as decorator

    def add_object(self, obj):
        prefix = obj.__class__.__name__.lower() + '.'
        self.build_method_map(obj, prefix)

    def add_dict(self, dict, prefix=''):
        if prefix:
            prefix += '.'
        self.build_method_map(dict, prefix)

    def add_method(self, f, name=None):
        """ Add a method to the dispatcher.

        Parameters
        ----------
        f : callable
            Callable to be added.
        name : str, optional
            Name to register (the default is function **f** name)

        Notes
        -----
        When used as a decorator keeps callable object unmodified.

        Examples
        --------

        Use as method

        >>> d = Dispatcher()
        >>> d.add_method(lambda a, b: a + b, name="sum")
        <function __main__.<lambda>>

        Or use as decorator

        >>> d = Dispatcher()
        >>> @d.add_method
            def mymethod(*args, **kwargs):
                print(args, kwargs)

        >>> @d.add_method(name='MyMethod')
            def mymethod(*args, **kwargs):
                print(args, kwargs)

        """
        if isinstance(f, six.string_types):
            name, f = f, name

        if f is None:
            # Be decorator generator
            def _add_method(f):
                return self.add_method(f, name)
            return _add_method

        self[name or f.__name__] = f
        return f

    def build_method_map(self, prototype, prefix=''):
        """ Add prototype methods to the dispatcher.

        Parameters
        ----------
        prototype : object or dict
            Initial method mapping.
            If given prototype is a dictionary then all callable objects will
            be added to dispatcher.
            If given prototype is an object then all public methods will
            be used.
        prefix: string, optional
            Prefix of methods

        """
        rpc_exports = getattr(prototype, 'rpc_exports', None)

        def _should_export(method):
            if method.startswith('_'):
                return False
            if rpc_exports is None:
                return True
            return method in rpc_exports

        if not isinstance(prototype, dict):
            prototype = dict((method, getattr(prototype, method))
                             for method in dir(prototype)
                             if _should_export(method))

        for attr, method in prototype.items():
            if callable(method):
                self[prefix + attr] = method
