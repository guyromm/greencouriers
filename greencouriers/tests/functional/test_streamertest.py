from greencouriers.tests import *

class TestStreamertestController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='streamertest', action='index'))
        # Test response...
