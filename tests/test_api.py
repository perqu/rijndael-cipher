import unittest
from fastapi.testclient import TestClient
from main import app


class TestCipherAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_encode_with_valid_key(self):
        key = "0123456789abcdef"
        response = self.client.get(f"/encode?message=Hello&key={key}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Response", response.json())

    def test_encode_with_invalid_key(self):
        key = "0123456789abcde"
        response = self.client.get(f"/encode?message=Hello&key={key}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["KEY not accepted"])

    def test_decode_with_valid_key(self):
        key = "0123456789abcdef"
        response = self.client.get(
            f"/decode?message=207 97 215 47 91 50 229 127 35 142 125 151 113 253 245 178&key={key}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Response", response.json())

    def test_decode_with_invalid_key(self):
        key = "0123456789abcde"
        response = self.client.get(
            f"/decode?message=207 97 215 47 91 50 229 127 35 142 125 151 113 253 245 178&key={key}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["KEY not accepted"])


if __name__ == "__main__":
    unittest.main()
