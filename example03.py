# example03.py
#
# Overriding of dependencies for testing purposes
# Keep in mind, overriding of a given dependency should be done before any object that relies on that dependency is
# instantiated
#
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
