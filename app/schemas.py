from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
  title:str
  content:str              
  published:bool=True
  
# class CreatePost(BaseModel):     #consist all the fields while creating posts
#   title:str
#   content:str              
#   published:bool=True
  
# class UpdatePost(BaseModel):   #for creating different model request we create some more classes
#   # title:str
#   # content:str              
#   published:bool          #user is only restricted to update published column only
  
class PostBase(BaseModel):   #by inheriting all attributes from PostBase def we need not to give columns in that Post(postBase)
  title:str      
  content:str
  published:bool=True

class PostCreate(PostBase):      #pydantic model by default it going to automatically inherit all the fields for PostBase
  pass             #same as PostBase

class Post(PostBase):   #we are defining the schema of the data that should appear in response and it consist of all the attributes in PostBase
  id:int
  # title:str   #commented bcs it already defined in PostBase
  # content:str
  # published:bool
  created_at:datetime
  class config():    #it going to say tell pydantic that ignore the fact that it is not a dict and go and convert into dict
    orm_mode=True
  
