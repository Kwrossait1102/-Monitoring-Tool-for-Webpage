import os, sys
os.environ["DATABASE_URL"] = "sqlite:///./test.db"  
os.environ["DISABLE_BACKGROUND"] = "1"

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app  # Import the FastAPI app from the package

from app.to_database import init_db
init_db()  # 显式建表一次

client = TestClient(app)


def _fake_response(status=200, body=b"OK"):
    """Mock HTTP response object"""
    r = MagicMock()
    r.ok = (200 <= status < 400)
    r.status_code = status
    r.content = body
    r.iter_content.return_value = iter([b"O"])
    return r


@patch("app.main.requests.get")
def test_root_endpoint_basic(mock_get):
    """Basic test: ensure '/' endpoint returns expected fields"""
    mock_get.return_value = _fake_response(200, b"hello")

    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()

    # Validate essential fields
    assert data.get("url")
    assert isinstance(data.get("available"), bool)
    assert "latency_ms" in data
    assert "ttfb_ms" in data
    assert "response_size_bytes" in data
