from greencouriers.tests import *

class TestCourierSignup2Controller(TestController):

    def test_index(self):
        response = self.app.get(url(controller='courier_signup_2', action='index'))
        # Test response...
