
from app import schemas
from .database import client,session
import pytest

@pytest.fixture
def test_user():
    user_data = {'email':"123@gmail.com",
                 'password':123123}
    res = client.post("/users/",json = user_data)

    assert res.status_code == 201


def test_create_user(client):
    res = client.post('/users/',json={'email':"hello1@gmail.com","password":"password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'hello1@gmail.com'
    assert res.status_code == 201


def test_login(client):
    res = client.post('/login',data={'username':'hello1@gmail.com','password':'password123'})

    assert res.status_code == 200

