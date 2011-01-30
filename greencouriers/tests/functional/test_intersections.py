from greencouriers.tests import *

class TestIntersectionsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='intersections', action='index'))
        # Test response...
