from greencouriers.tests import *

class TestCourierSignupController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='courier_signup', action='index'))
        # Test response...
