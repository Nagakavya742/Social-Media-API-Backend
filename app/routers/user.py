from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oauth2     #.. means importing file from other upper folder
from sqlalchemy.orm import  Session
from .. database import get_db   #. means importing file from same dir or folder

router=APIRouter(
  prefix="/users",
  tags=['Users']
)
# POSTGRES DATABASE
#connecting postgres to python with Psycopg2

    #WORKING WITH USER DATA
    

# @router.get("/me")
# def get_me(current_user=Depends(oauth2.get_current_user)):
#     return current_user
  
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)  #schemas.UserOut says that the output that is response-model should be executed as per UserOut definition
def create_post(user:schemas.UserCreate,db:Session = Depends(get_db)):
  
  #hash the password - user.password
  hashed_password=utils.hash(user.password)   #hashed the user password
  user.password = hashed_password
  new_user=models.User(     #it is used to retrieve all attributes(column) in DataBase table
    **user.dict()
  )
  db.add(new_user)   #added to newly created DB
  db.commit()
  db.refresh(new_user)    #returning the posts to PgAdmin same as returning statement in psycopg2 and sqlalchemy model
  return new_user    #just to return the data in JSON files and only the required data
  #it separately gives random is=d to every post inserted into it
  #thus by running get method we get all the posts send to the post_dict
    #given all values in dict
  

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id: int,db:Session = Depends(get_db)):
  user=db.query(models.User).filter(models.User.id==id).first()
  
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} does not exist")
  return user