from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app=FastAPI()   #FastAPI is in child level so first in Social-Media-API-Backend activate it and then cd app excute and database is connected


      #SCHEMA
class Post(BaseModel):
  title:str
  content:str              
  published:bool=True
  
  
while True:
  try:
    conn=psycopg2.connect(
      host='localhost',                  #local host is defined for local machine for ip address
      database='fastAPI',                #My DB is fastAPI and it connects
      user='postgres',                   #it connects to the postgres user
      password='pavan',             #password for PgAdmin change it while commiting into github
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
    
  
@app.get("/")
def get_posts():
  return {"dat" : "this is your posts"}

    #CRUD OPP
     # GETTING ALL POSTS
@app.get("/posts")         
def get_posts():
  cursor.execute("""SELECT * FROM posts""")
  posts=cursor.fetchall()
  return {"data":posts}


    #CREATING POSTS
@app.post("/posts", status_code=status.HTTP_201_CREATED) #changes the default 200 as 201 created
def create_posts(post:Post):         
  #referencing pydantic model
  # instead of dict we use model_dump in pydantic
  cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """,
                 (post.title,post.content,post.published))   #getting values
  conn.commit()   #make sure to connect commit to actual postgres database
  new_post=cursor.fetchone()
  return {"data":new_post} 
  #it separately gives random is=d to every post inserted into it
  #thus by running get method we get all the posts send to the post_dict
    #given all values in dict
    
    
# @app.get("/posts/latest")
# def get_latest_post():
#   post=my_posts[len(my_posts)-1]        #order matter while building api
#   return{"detail":post}


    #GETTING INDIVIDUAL POSTS
@app.get("/posts/{id}")         
#id represents the path parameter id of specific post
def get_post(id:str,response:Response):     #changing the response of the error occured like 200 to 404    
  #automatically converts the the inbuilt string into int
  cursor.execute("""SELECT * FROM posts where id=%s""",(str(id)))
  post=cursor.fetchone()
  
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
    # response.status_code=status.HTTP_404_NOT_FOUND   #changes the error code from 200 to 404  and inbuilt package provides the status of the error
    # return{'message':f"post with id: {id} was not found"}
  return {"post_detail":post}

     #DELETE THE POSTS
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)   #directly updating the status code by giving it in the decorator
def delete_post(id:str):
  #deleting post
  #find the index of the array that has replaced ID
  #my_posts.pop(index)
  cursor.execute("""DELETE FROM posts where id=%s returning *""",(str(id),))
  deleted_post=cursor.fetchone()
  conn.commit()
  
  
  if deleted_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)
  
    #UPDATING THE POST
@app.put("/posts/{id}")
def update_post(id: int,post: Post):
  cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s where id=%s RETURNING *""",
                 (post.title,post.title,post.published,str(id)))
  updated_post=cursor.fetchone()
  conn.commit()
  
  if updated_post == None:      #Works with def function
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} does not exist")
  
  
  return {"data":updated_post}
  
  
  
#while executing the fastapi in Swagger we should fetch data and run it by using uvicorn main:app --reload
  #SCHEMA
  
# POSTGRE DATABASE
#connecting postgre to python with Psycopg2



  

  
  
      
  
  
          

