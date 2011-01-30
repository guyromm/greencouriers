from greencouriers.tests import *

class TestBusinessController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='business', action='index'))
        # Test response...
