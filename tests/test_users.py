from app import schemas
from .database import session , client




def test_create_user(client):
    response = client.post("/users", json={"username": "test", "email": "test@email.com" , "password": "test"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "test@email.com"
    assert response.status_code == 201

def test_login_user(client):
    response = client.post("/login", data={"username": "test@email.com" , "password": "test"})
    assert response.status_code == 200