from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional,List
# from random import randrange

# from sqlalchemy.orm import  Session
# from app.models import models
from .database import engine   #. means importing file from same dir or folder
# from . import models,schemas,utils
from . routers import post, user, auth ,vote
from . import models
from . config import settings   #importing settings instance variable from config

models.Base.metadata.create_all(bind=engine)   # it says sqlalchemy to run create statements so that it generates all of the tables


app=FastAPI()   #FastAPI is in child level so first in Social-Media-API-Backend activate it and then cd app execute and database is connected

origins=["*"]             #origins=["https://www.google.com","https://www.youtube.com"]   #allow google to talk with us list of url's that can talk to our API    origins=["*"] it means allowing every single origin to access our API

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],          #all methods can be retrieved
  allow_headers=["*"]           #all headers can be retrieved
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




# def find_post(id):
#   for p in my_posts:
#     if p['id'] == id:
#       return p
    
# def find_index_post(id):
#   for i,p in enumerate(my_posts):
#     if p['id'] == id:
#       return i
    

@app.get("/")
def root():
  return {"data" : "this is your posts"}

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
  
