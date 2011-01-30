from greencouriers.tests import *

class TestActivitiesAdminController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='activities_admin', action='index'))
        # Test response...
