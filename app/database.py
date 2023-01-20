from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:' \
                          f'{settings.database_password}@' \
                          f'{settings.database_hostname}:' \
                          f'{settings.database_port}/' \
                          f'{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

#while True:

   # try:
   #     conn = psycopg2.connect(host = 'localhost',database ='fastapi',user = 'postgres',password ='7861',cursor_factory=RealDictCursor)
      #  cursor = conn.cursor()
     #   print('dbdone')
     #   break
   # except Exception as error:
     #   print('failed to connect', error)
     #   time.sleep(2)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()