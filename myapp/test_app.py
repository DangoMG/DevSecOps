import unittest
from app import app

class TestCalcUI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_add(self):
        response = self.client.post("/", data={"a": "2", "b": "3", "operation": "add"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Result: 5", response.data)

    def test_subtract(self):
        response = self.client.post("/", data={"a": "5", "b": "3", "operation": "subtract"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Result: 2", response.data)

if __name__ == "__main__":
    unittest.main()
