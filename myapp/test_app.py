import unittest
from app import app

class TestCalcAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add(self):
        response = self.app.get("/add?a=2&b=3")
        self.assertEqual(response.json['result'], 5)

    def test_subtract(self):
        response = self.app.get("/subtract?a=5&b=3")
        self.assertEqual(response.json['result'], 2)

if __name__ == "__main__":
    unittest.main()
