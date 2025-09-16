from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_account():
    response = client.post("/accounts/", json={"name": "John"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John"
    assert data["balance"] == 0.0
