from greencouriers.tests import *

class TestTesticleController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='testicle', action='index'))
        # Test response...
