from app import schemas
import pytest
from jose import jwt
from app.config import settings



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