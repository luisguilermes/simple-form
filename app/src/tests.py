import unittest
import simpleform

#olhar pagina 142
class TestCase(unittest.TestCase):
    def setUp(self):
        simpleform.app.config["TESTING"] = True
        self.app = simpleform.app.test_client()

    def test_get_apiinfo(self):
        apiinfo = simpleform.app.test_request

