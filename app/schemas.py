from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime
from typing import Optional
from pydantic.types import conint

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
  # Post:Post
  # votes:int
  title:str      
  content:str
  published:bool=True
  model_config=ConfigDict(from_attributes=True)

class PostCreate(PostBase):      #pydantic model by default it going to automatically inherit all the fields for PostBase
  pass             #same as PostBase

class UserOut(BaseModel):
  id:int
  email:EmailStr
  created_at:datetime
  model_config=ConfigDict(from_attributes=True)
    
class Post(PostBase):   #we are defining the schema of the data that should appear in response and it consist of all the attributes in PostBase
  
  id:int
  # title:str   #commented bcs it already defined in PostBase
  # content:str
  # published:bool
  created_at:datetime
  owner_id:int
  owner:UserOut    #it returns the pydantic model
  votes:Optional[int] = 0  #vote count for the post
  
  model_config=ConfigDict(from_attributes=True)
  
class PostOut(BaseModel):
  Post:Post
  votes:int
  
  model_config=ConfigDict(from_attributes=True)
  
class UserCreate(BaseModel):
  email : EmailStr  #default email validator in pydantic lib checks if it is a valid email
  password : str
  

    
class UserLogin(BaseModel):
  email:EmailStr
  password:str
  
class Token(BaseModel):
  access_token:str
  token_type:str

class TokenData(BaseModel):
  id:Optional[str]=None
  
class Vote(BaseModel):
  post_id:int
  dir: conint(le=1)
  