import functools
import types
from inspect import isclass


class Di:

    def __init__(self, di=None):
        """
        Initialize internal variables
        """
        self._parent = di
        self._registry = {}  # internal dependency registry

    def register(self, name: str):
        """
        Decorator to register classes
        :param name:
        :return: wrapper function for registered item
        """

        def wrap(fn):  # wrapper function to be detected as callable for the registered class
            self.add(name, fn)

        return wrap

    def override(self, name: str):
        """
        Override a dependency definition
        :param name:
        :return: wrapper function for registered item
        """

        def wrap(fn):  # wrapper function to be detected as callable for the registered class
            self.add(name, fn, True)

        return wrap

    def add(self, name: str, item, replace=False):
        """
        Adds a new item to the registry
        :param name:
        :param item:
        :param replace:
        :return:
        """
        if self.has(name) and not replace:
            raise RuntimeError("Dependency name '{}' already in use".format(name))

        if isclass(item):
            def cls_wrap(_di):  # if it is a class, we'll create a wrap function to instantiate the object
                return item(_di)

            self._registry[name] = cls_wrap  # store the wrapper class
        else:
            self._registry[name] = item  # or if it is an object or callable, just store it
        if replace:  # if replacing existing item, clear lru_cache
            self.get.cache_clear()

    @functools.lru_cache(maxsize=None)
    def get(self, name: str):
        """
        Retrieve a dependency from the registry by name
        - If dependency exists as a function or lambda, the result of the function replaces the registry contents
        :param name: dependency name
        :return: dependency object
        """
        if not self.has(name):
            if self._parent is not None:
                return self._parent.get(name)
            raise RuntimeError("Key '{}' not found in the registry".format(name))

        item = self._registry[name]

        # if callable, lets execute and use the result instead
        # and replace the stored item with the result of the callable
        # if class, just instantiate the class
        if type(item) in [types.LambdaType, types.FunctionType]:
            item = item(self)
            self._registry.pop(name)  # remove 'factory' or wrapper reference
            self._registry[name] = item  # replace it with the actual object

        return item

    def scope(self, name: str):
        """
        Create a scoped DI instance
        :param name:
        :return:
        """
        result = Di(self)
        self.add(name, result)
        return result

    def has(self, name: str) -> bool:
        """
        Verifies if a given name exists in the registry
        :param name:
        :return:
        """
        return name in self._registry.keys()

    def keys(self) -> list:
        """
        Retrieve a list of all registered names
        :return:
        """
        return list(self._registry.keys())

    def remove(self, name: str):
        """
        Removes a registered dependency
        :param name:
        :return:
        """
        if self.has(name):
            del self._registry[name]
            # clear lru_cache cache
            self.get.cache_clear()
        else:
            raise RuntimeError("Dependency name '{}' not found in the registry".format(name))

