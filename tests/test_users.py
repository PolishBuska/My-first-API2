from jose import jwt
from app import schemas
from app.config import settings
import pytest




def test_create_user(client):
    res = client.post('/users/',json={'email':"hello1@gmail.com","password":"password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'hello1@gmail.com'
    assert res.status_code == 201

@pytest.mark.parametrize("email, password, status_code",[
    ('wrong@gmail.com','111', 406),
    ('wrong@gmail.com',None,422),
    (None,"pASS",422)])
def test_wrong_password_user_create(client,email,password,status_code):
    res = client.post('/users/', json={'email': email,'password': password})
    assert res.status_code == status_code


def test_login(client,test_user):
    res = client.post('/login',data={'username':f"{test_user['email']}",'password':f'{test_user["password"]}'})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ('wrong@gmail.err','111111', 403),
    ('wrong@gmail.com',None,422),
    (None,"pASS",422)
])
def test_incorrect_login(test_user,client,email,password,status_code):
    res = client.post('/login',data ={"username":email ,"password":password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid credentials'