from app import schemas
from .database import session , client
import pytest
from jose import jwt
from app.config import settings


@pytest.fixture(scope="function")
def test_user(client):
    user_data = {
        "username": "m",
        "email": "m@email.com",
        "password": "password123",
    }
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


def test_create_user(client):
    response = client.post("/users", json={"username": "test", "email": "test@email.com" , "password": "test"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "test@email.com"
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user['email'] , "password": test_user['password']})
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    id  = payload.get("user_id")
    assert response.status_code == 200
    assert login_res.token_type == "bearer"
    assert id == test_user['id']