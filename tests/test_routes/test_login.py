from fastapi.testclient import TestClient

from api import login

client = TestClient(login)


def test_authenticate_users():
    response = client.get("/authenticate")
    assert response.status_code == 200
    #assert response.json() == {"msg": "Hello World"}