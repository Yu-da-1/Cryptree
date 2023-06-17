import json
import unittest
from server import app 

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data, b'Hello World')

if __name__ == "__main__":
    unittest.main()