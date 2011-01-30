from greencouriers.tests import *

class TestParseTownsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='parse_towns', action='index'))
        # Test response...
