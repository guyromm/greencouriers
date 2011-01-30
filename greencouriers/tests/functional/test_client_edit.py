from greencouriers.tests import *

class TestClientEditController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='client_edit', action='index'))
        # Test response...
