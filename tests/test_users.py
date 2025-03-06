from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)


def test_create_user():
    response = client.post("/users", json={"username": "test", "email": "test3@email.com" , "password": "test"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "test3@email.com"
    assert response.status_code == 201
