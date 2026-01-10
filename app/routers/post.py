from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models, oauth2,schemas    #.. means importing file from other upper folder
from sqlalchemy.orm import  Session
from .. database import get_db   #. means importing file from same dir or folder
from typing import List

router=APIRouter(
  prefix="/posts",
  tags=['posts']
)

@router.get("/",response_model=List[schemas.Post])      #since the dat is dict so we converting into List  
def get_posts(db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):   #ur path operations need to work with DB then u should give parameters db:session=Depends(get_db)
  # cursor.execute("""SELECT * FROM posts""")
  # posts=cursor.fetchall()
  posts=db.query(models.Post).all()
  return posts




    #CREATING POSTS
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post) #changes the default 200 as 201 created  pydantic works with dict only
def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):         
  #referencing pydantic model
  # instead of dict we use model_dump in pydantic
  # cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """,
  #                (post.title,post.content,post.published))   #getting values
  # conn.commit()   #make sure to connect commit to actual postgres database
  # new_post=cursor.fetchone()
  # print(**post.dict())
  # new_post=models.Post(title=post.title,
  #                      content=post.content,
  #                      published=post.published)  #sqlalchemy handles all our logics and retrieving data
  new_post=models.Post(     #it is used to retrieve all attributes(column) in DataBase table
    **post.dict()
  )
  print(current_user.email)
  db.add(new_post)   #added to newly created DB
  db.commit()
  db.refresh(new_post)    #returning the posts to PgAdmin same as returning statement in psycopg2 and sqlalchemy model
  return new_post    #just to return the dat in JSON files and only the required data
  #it separately gives random is=d to every post inserted into it
  #thus by running get method we get all the posts send to the post_dict
    #given all values in dict
    
    
# @app.get("/posts/latest")
# def get_latest_post():
#   post=my_posts[len(my_posts)-1]        #order matter while building api
#   return{"detail":post}




    #GETTING INDIVIDUAL POSTS
@router.get("/{id}",response_model=schemas.Post)  #getting response from schemas.Post       
#id represents the path parameter id of specific post
def get_post(id:int,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):     #(response:Response)changing the response of the error occurred like 200 to 404    
  #automatically converts the the inbuilt string into int
  # cursor.execute("""SELECT * FROM posts where id=%s""",(str(id)))
  # post=cursor.fetchone()
  post=db.query(models.Post).filter(models.Post.id == id).first()   #since we know that it contains only one post with unique id so instead of all() we can use first so one value is given
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
    # response.status_code=status.HTTP_404_NOT_FOUND   #changes the error code from 200 to 404  and inbuilt package provides the status of the error
    # return{'message':f"post with id: {id} was not found"}
  return post




     #DELETE THE POSTS
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)   #directly updating the status code by giving it in the decorator
def delete_post(id:int,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
  #deleting post
  #find the index of the array that has replaced ID
  #my_posts.pop(index)
  # cursor.execute("""DELETE FROM posts where id=%s returning *""",(str(id),))
  # deleted_post=cursor.fetchone()      #sql code
  # conn.commit()
  
  post=db.query(models.Post).filter(models.Post.id == id)
  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
  post.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
  
  
  
  
    #UPDATING THE POST
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int,post_data: schemas.PostCreate,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):    #importing Post from schemas so schemas.Post
  # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s where id=%s RETURNING *""",
  #                (post.title,post.title,post.published,str(id)))
  # updated_post=cursor.fetchone()   #postgres code
  # conn.commit()
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if post == None:      #Works with def function
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} does not exist")
  
  post_query.update(post_data.model_dump(),synchronize_session=False)   #dict() is Pydantic v2 does ot work on sqlalchemy model
  
  db.commit()   #commit it to database
  
  return post_query.first() #after updating post and send it back to user    removed {"data":} because we just return only content not data
  