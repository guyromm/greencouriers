from greencouriers.tests import *

class TestCourierController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='courier', action='index'))
        # Test response...
