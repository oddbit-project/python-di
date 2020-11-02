# example02.py
#
# Custom factory Usage - factories are registered via @di.register() decorator, and class constructor may receive
# external dependencies explicitly upon creation. This traditional approach to di doesn't benefit from lazy loading
# of specific dependencies
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


svc = di.get('service')  # instantiate 'service' and 'dependency' via factory
svc.run()  # print message
