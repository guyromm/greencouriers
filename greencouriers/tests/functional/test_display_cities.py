from greencouriers.tests import *

class TestDisplayCitiesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='display_cities', action='index'))
        # Test response...
