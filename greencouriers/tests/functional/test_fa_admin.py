from greencouriers.tests import *

class TestFaAdminController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='fa_admin', action='index'))
        # Test response...
