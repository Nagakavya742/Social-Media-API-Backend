from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import  Session

# from app.models import models
from .database import engine,get_db   #. means importing file from same dir or folder
from . import models,schemas,utils
from . routers import post,user


models.Base.metadata.create_all(bind=engine)


app=FastAPI()   #FastAPI is in child level so first in Social-Media-API-Backend activate it and then cd app execute and database is connected





      #SCHEMA

  
  
while True:
  try:
    conn=psycopg2.connect(
      host='localhost',                  #local host is defined for local machine for ip address
      database='fastAPI',                #My DB is fastAPI and it connects
      user='postgres',                   #it connects to the postgres user
      password='pavan@5701', #password for PgAdmin change it while committing into github
      cursor_factory=RealDictCursor)     #it gives the column names and values
    cursor=conn.cursor()
    print("Database connection was successful")
    break

  except Exception as error:
    
    print("Connecting to database failed")
    print("error:",error)
    break
    

  
my_posts=[{"title":"title of the post 1","content":"content of post 1","id":1},
          {"title":"favorite food","content":"I like Pizza","id":2}]

def find_post(id):
  for p in my_posts:
    if p['id'] == id:
      return p
    
def find_index_post(id):
  for i,p in enumerate(my_posts):
    if p['id'] == id:
      return i
    
    
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def get_posts():
  return {"dat" : "this is your posts"}

# @app.get("/sqlalchemy")     # it is used while learning sqlalchemy
# def test_posts(db:Session = Depends(get_db)):
#   posts=db.query(models.Post)  #model represents table and db represents SessionLocal in DB
#                               #same as select * from posts.It abstracts all sql queries         
#   print(posts)
#   return {"data":"successful"}




    #CRUD OPP
     # GETTING ALL POSTS

  
  
#while executing the fastapi in Swagger we should fetch data and run it by using uvicorn main:app --reload
  #SCHEMA
  
