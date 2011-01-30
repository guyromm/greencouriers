from greencouriers.tests import *

class TestBusinessEditController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='business_edit', action='index'))
        # Test response...
