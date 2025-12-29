from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
app=FastAPI()

class Post(BaseModel):
  title:str
  content:str
  published:bool=True
  rating:Optional[int]=None

@app.get("/")
def get_posts():
  return {"data" : "this is your posts"}
@app.get("/posts")
async def root():
  return {"message":"Welcome to my API!!!"}

@app.post("/createposts")
def create_posts(post:Post):   #referencing pydantic model
  print(post.rating)
  print(post.dict())   #given all values in dict
  return {"data":post}

#title str, content str
          

