# example01.py
#
# Simple Usage - registration is done via @di.register() decorator, and class constructor *always* receives di as first
# parameter upon creation. This has the advantage of benefiting from lazy loading by placing the retrieving of dependencies
# near the place they are used
#
from di import di


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
