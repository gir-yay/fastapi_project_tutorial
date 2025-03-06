import pytest

from fastapi.testclient import TestClient
from app.main import app
from app import schemas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
from app.database import get_db, Base

#SQLALCHEMY_DATABASE_URL = "postgresql://user:secret@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_ROOT_USER}:{settings.DATABASE_ROOT_PASSWORD}@{settings.DATABASE_URL}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db




#client = TestClient(app)

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)



def test_create_user(client):
    response = client.post("/users", json={"username": "test", "email": "test@email.com" , "password": "test"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "test@email.com"
    assert response.status_code == 201
