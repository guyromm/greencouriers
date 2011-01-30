from greencouriers.tests import *

class TestMatchesMapController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='matches_map', action='index'))
        # Test response...
