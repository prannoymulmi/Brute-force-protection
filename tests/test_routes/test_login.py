from fastapi.testclient import TestClient
from config.models.ProjectSettings import ProjectSettings
from main import app

client = TestClient(app)


def test_authenticate_users():
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate", json={"username": "testUser", "password": "testPassword"})
    assert response.status_code == 200
    #assert response.json() == {"msg": "Hello World"}