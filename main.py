from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app=FastAPI()


      #SCHEMA
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
  return {"data":my_posts}


    #CREATING POSTS
@app.post("/posts", status_code=status.HTTP_201_CREATED) #changes the default 200 as 201 created
def create_posts(post:Post):         
  #referencing pydantic model
  # instead of dict we use model_dump in pydantic
  post_dict=post.model_dump()    
  post_dict['id']=randrange(0, 1000000)
  my_posts.append(post_dict)
  return {"data":post_dict}      
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
def get_post(id: int,response:Response):     #changing the response of the error occured like 200 to 404    
  #automatically converts the the inbuilt string into int
  post=find_post(id)
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
    # response.status_code=status.HTTP_404_NOT_FOUND   #changes the error code from 200 to 404  and inbuilt package provides the status of the error
    # return{'message':f"post with id: {id} was not found"}
  return {"post_detail":post}

     #DELETE THE POSTS
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)   #directly updating the status code by giving it in the decorator
def delete_post(id:int):
  #deleting post
  #find the index of the array that has replaced ID
  #my_posts.pop(index)
  index=find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
  my_posts.pop(index)
  return Response(status_code=status.HTTP_204_NO_CONTENT)
  
    #UPDATING THE POST
@app.put("/posts/{id}")
def update_post(id: int,post: Post):
  index=find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} does not exist")
  
  post_dict=post.model_dump()
  post_dict['id']=id           #newly id key is added to post
  my_posts[index]=post_dict
  return {"data":post_dict}
  
  #SCHEMA
  
      
  
  
          

