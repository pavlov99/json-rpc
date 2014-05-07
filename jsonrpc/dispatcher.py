import collections


class Dispatcher(collections.MutableMapping):

    """ Method dispatcher.

    Dictionary like object which holds map method_name to method.

    """

    def __init__(self, prototype=None):
        """ Build method dispatcher.

        :param prototype: Initial method mapping.
        :type prototype: None or object

        """
        self.method_map = dict()

        if prototype is not None:
            self.build_method_map(prototype)

    def __getitem__(self, key):
        return self.method_map[key]

    def __setitem__(self, key, value):
        self.method_map[key] = value

    def __delitem__(self, key):
        del self.method_map[key]

    def __len__(self):
        return len(self.method_map)

    def __iter__(self):
        return iter(self.method_map)

    def add_method(self, f, name=None):
        """ Add a method to the dispatcher.

        :param callable f: Callable to be added.
        :param name: Name to register
        :type name: None or str

        """
        self.method_map[name or f.__name__] = f

    def build_method_map(self, prototype):
        """ Add prototype methods to the dispatcher.

        :param prototype: Method mapping.
        :type prototype: None or object

        All public prototype methods can be accessed using dispatcher.

        """
        methods = [method for method in dir(prototype)
                   if not method.startswith('_')]

        for method in methods:
            attr = getattr(prototype, method)

            if callable(attr):
                self[method] = attr
