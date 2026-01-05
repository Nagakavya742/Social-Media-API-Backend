from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL='postgresql://postgres:pavan@localhost/fastAPI'
SQLALCHEMY_DATABASE_URL='postgresql://postgres:pavan@localhost/fastAPI'

engine=create_engine(SQLALCHEMY_DATABASE_URL)     #engine is responsible for sqlalchemy to connect to postgres database

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)    #actually talk to sql DBwe use sessionmaker

Base=declarative_base()

#defining all DB models using python and ORM's

def get_db():    #we just keep calling this function every time we get any request from to any of our API endpoints 
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()