from greencouriers.tests import *

class TestClientSignupController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='client_signup', action='index'))
        # Test response...
