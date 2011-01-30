from greencouriers.tests import *

class TestMyAccountController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='my_account', action='index'))
        # Test response...
