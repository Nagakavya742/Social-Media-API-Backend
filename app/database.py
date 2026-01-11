from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


# SQLALCHEMY_DATABASE_URL='postgresql://postgres:pavan@localhost/fastAPI'
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

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
  
  # while True:
  #   try:
  #     conn=psycopg2.connect(
  #       host='localhost',                  #local host is defined for local machine for ip address
  #       database='fastAPI',                #My DB is fastAPI and it connects
  #       user='postgres',                   #it connects to the postgres user
  #       password='pavan', #password for PgAdmin change it while committing into github
  #       cursor_factory=RealDictCursor)     #it gives the column names and values
  #     cursor=conn.cursor()
  #     print("Database connection was successful")
  #     break

  #   except Exception as error:
      
  #     print("Connecting to database failed")
  #     print("error:",error)
  #     break