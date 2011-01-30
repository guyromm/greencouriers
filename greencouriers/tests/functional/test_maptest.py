from greencouriers.tests import *

class TestMaptestController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='maptest', action='index'))
        # Test response...
