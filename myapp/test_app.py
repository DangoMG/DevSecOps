import unittest
from app import app
import json

class TestCalcAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_add(self):
        response = self.client.post("/api/calc", 
            data=json.dumps({"a": 2, "b": 3, "operation": "add"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 5)

    def test_subtract(self):
        response = self.client.post("/api/calc", 
            data=json.dumps({"a": 5, "b": 3, "operation": "subtract"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 2)

if __name__ == "__main__":
    unittest.main()
