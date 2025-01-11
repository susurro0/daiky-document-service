import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app

class TestCreateApp(unittest.TestCase):
    def test_app_instance(self):
        self.assertIsInstance(app, FastAPI)

    def test_app_creation(self):
        self.assertIsNotNone(app)

    def test_read_root(self):
        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello, World!"})

if __name__ == '__main__':
    unittest.main()