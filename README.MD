# di

Minimalist dependency injection library for Python 3.x

### Requirements
  - python >= 3.7 (may work with previous versions) 
  - pytest 
  
### Usage  

##### Using global registry-style dependencies
Import di variable from the library and register dependencies by using the provided decorator:
```python
@di.register('dependency')
class Dependency:

    def __init__(self, di):
        pass

    def action(self):
        print("Hello from dependency")


@di.register('service')
class Service:

    def __init__(self, di):
        self._di = di
        self._dependency = None

    def run(self):
        self.get_dependency().action()

    def get_dependency(self):
        if self._dependency is None:
            # dependency is only built & instantiated at this point
            self._dependency = self._di.get('dependency')
        return self._dependency


svc = di.get('service')  # instantiate 'service', but not 'dependency' yet,as it was not referenced
svc.run()  # instantiate 'dependency' and print message
```

##### Using traditional di approach with a custom factories
Import di variable and register your factories using the provided decorator:
```python
from di import di


@di.register('dependency')
class Dependency:

    def __init__(self, di):
        pass

    def action(self):
        print("Hello from dependency")


class Service:

    def __init__(self, dep: Dependency):
        self._dependency = dep

    def run(self):
        self._dependency.action()


@di.register('service')
def service_factory(_di):
    # retrieve dependency from di and inject into Service() instance
    return Service(_di.get('dependency'))


svc = di.get('service')  # instantiate 'service' and 'dependency' via factory
svc.run()  # print message
```python
from di import di


@di.register('dependency')
class Dependency:

    def __init__(self, di):
        pass

    def action(self):
        print("Hello from dependency")


class Service:

    def __init__(self, dep: Dependency):
        self._dependency = dep

    def run(self):
        self._dependency.action()


@di.register('service')
def service_factory(_di):
    # retrieve dependency from di and inject into Service() instance
    return Service(_di.get('dependency'))


# override existing 'dependency' definition
@di.override('dependency')
class MockedDependency:

    def __init__(self, di):
        pass

    def action(self):
        print("Hello from mocked dependency")

svc = di.get('service')  # instantiate 'service' and 'dependency' via factory
svc.run()  # print message from mocked dependency
```

### License

This package is provided under a 2-clause BSD License. See LICENSE for details.

