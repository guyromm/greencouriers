from greencouriers.tests import *

class TestDeluserController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='deluser', action='index'))
        # Test response...
