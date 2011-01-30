from greencouriers.tests import *

class TestScheduleIntersectionsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='schedule_intersections', action='index'))
        # Test response...
