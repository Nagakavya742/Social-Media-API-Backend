from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app=FastAPI()

class Post(BaseModel):
  title:str
  content:str
  published:bool=True
  rating:Optional[int]=None
  
my_posts=[{"title":"title of the post 1","content":"content of post 1","id":1},
          {"title":"favorite food","content":"I like Pizza","id":2}]

def find_post(id):
  for p in my_posts:
    if p['id'] == id:
      return p
    


@app.get("/")
def get_posts():
  return {"dat" : "this is your posts"}

@app.get("/posts")
def get_posts():
  return {"data":my_posts}

@app.post("/posts")
def create_posts(post:Post):     #referencing pydantic model
  # instead of dict we use model_dump in pydantic
  post_dict=post.model_dump()    
  post_dict['id']=randrange(0, 1000000)
  my_posts.append(post_dict)
  return {"data":post_dict}      
  #it separately gives random is=d to every post inserted into it
  #thus by running get method we get all the posts send to the post_dict
    #given all values in dict

@app.get("/posts/{id}")    #id represents the path parameter id of specific post
def get_post(id: str):      #automatically converts the the inbuilt string into int
  post=find_post(id)
  print(post)
  return {"post_detail":post}
  
  
      
  
  
          

