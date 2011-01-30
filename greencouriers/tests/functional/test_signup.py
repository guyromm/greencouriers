from greencouriers.tests import *

class TestSignupController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='signup', action='index'))
        # Test response...
