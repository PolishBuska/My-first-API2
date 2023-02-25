from app.main import app
from fastapi.testclient import TestClient
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
import pytest
from app.JWT_SERVICE import create_acces_token
from alembic import command
from app import models
@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:7861@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:' \
                          f'{settings.database_password}@' \
                          f'{settings.database_hostname}:' \
                          f'{settings.database_port}/' \
                          f'{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

@pytest.fixture
def test_user(client):
    user_data = {'email':"123@gmail.com",
                 'password':123123}
    res = client.post("/users/",json = user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture
def token(test_user):
    return create_acces_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session):
    posts_data = [{
        "title":"firs title",
        "content": "first pass",
        "owner_id": test_user['id']
                   },{
        "title":"2nd title",
        "content": "2nd pass",
        "owner_id": test_user['id']
                   },{
        "title":"3rd title",
        "content": "3rd pass",
        "owner_id": test_user['id']
                   }]
    def create_post_model(post):
        return models.Post(**post)
    post_map = list(map(create_post_model,posts_data))
    session.add_all(post_map)
    session.commit()
    posts = session.query(models.Post).all()
    return posts