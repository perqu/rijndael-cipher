import pytest
from fastapi.testclient import TestClient
from main import app


class TestCipherAPI:
    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    def test_encode_with_valid_key(self):
        key = "0123456789abcdef"
        response = self.client.get(f"/encode?message=Hello&key={key}")
        assert response.status_code == 200
        assert "Response" in response.json()

    def test_encode_with_invalid_key(self):
        key = "0123456789abcde"
        response = self.client.get(f"/encode?message=Hello&key={key}")
        assert response.status_code == 200
        assert response.json() == ["KEY not accepted"]

    def test_decode_with_valid_key(self):
        key = "0123456789abcdef"
        response = self.client.get(
            f"/decode?message=207 97 215 47 91 50 229 127 35 142 125 151 113 253 245 178&key={key}"
        )
        assert response.status_code == 200
        assert "Response" in response.json()

    def test_decode_with_invalid_key(self):
        key = "0123456789abcde"
        response = self.client.get(
            f"/decode?message=207 97 215 47 91 50 229 127 35 142 125 151 113 253 245 178&key={key}"
        )
        assert response.status_code == 200
        assert response.json() == ["KEY not accepted"]


if __name__ == "__main__":
    pytest.main()
