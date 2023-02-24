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
from alembic import command

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

def test_root(client):
    res = client.get("/")
    print(res.json().get('Message'))
    assert res.json().get('Message') == 'Hello World'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post('/users/',json={'email':"hello1@gmail.com","password":"password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'hello1@gmail.com'
    assert res.status_code ==201

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:7861@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:' \
                          f'{settings.database_password}@' \
                          f'{settings.database_hostname}:' \
                          f'{settings.database_port}/' \
                          f'{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)



#while True:

   # try:
   #     conn = psycopg2.connect(host = 'localhost',database ='fastapi',user = 'postgres',password ='7861',cursor_factory=RealDictCursor)
      #  cursor = conn.cursor()
     #   print('dbdone')
     #   break
   # except Exception as error:
     #   print('failed to connect', error)
     #   time.sleep(2)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db]= override_get_db
