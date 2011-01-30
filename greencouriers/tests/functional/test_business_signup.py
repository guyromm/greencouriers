from greencouriers.tests import *

class TestBusinessSignupController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='business_signup', action='index'))
        # Test response...
