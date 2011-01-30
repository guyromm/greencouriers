from greencouriers.tests import *

class TestCourierEditController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='courier_edit', action='index'))
        # Test response...
