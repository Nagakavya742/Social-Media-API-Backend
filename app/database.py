from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL='postgresql://postgres:pavan@5701@localhost/fastAPI'
SQLALCHEMY_DATABASE_URL='postgresql://postgres:pavan@localhost/fastAPI'

engine=create_engine(SQLALCHEMY_DATABASE_URL)     #engine is responsible for sqlalchemy to connect to postgres database

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)    #actually talk to sql DBwe use sessionmaker

Base=declarative_base()

#defining all DB models using python and ORM's

def get_db():    #we just keep calling this function every time we get any request from to any of our API endpoints 
  
    # Dependency function that yields a database session object.
    # This function is a generator that yields a database session object.
    # It is used as a dependency in FastAPI endpoints to ensure that
    # a database session is created and closed for each incoming request.
    # The function uses a try/finally block to ensure that the database
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()