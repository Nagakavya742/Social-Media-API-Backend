from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models, oauth2,schemas    #.. means importing file from other upper folder
from sqlalchemy.orm import  Session
from .. database import get_db   #. means importing file from same dir or folder
from typing import List,Optional
from sqlalchemy import func

router=APIRouter(
  prefix="/posts",
  tags=['posts']
)

#@router.get("/",response_model=List[schemas.Post])   #since the dat is dict so we converting into List  it is to return posts
@router.get("/",response_model=List[schemas.PostOut])    # it is to return results
def get_posts(db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):   #ur path operations need to work with DB then u should give parameters db:session=Depends(get_db)
  # cursor.execute("""SELECT * FROM posts""")
  # posts=cursor.fetchall()
  print(search)
  print(limit)
  # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  #.filter(models.Post.owner_id==current_user.id).all()  #we r instructing to view posts only for the owner_id that creates posts not other 
  
  posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()        # it says that left outer joint to perform
  posts = list ( map (lambda x : x._mapping, posts) )
  print(posts)
  # Convert tuples to Post objects with votes
  # posts = []
  # for post, vote_count in results:
  #   # Use model_validate to convert SQLAlchemy model to Pydantic model, then add votes
  #   post_schema = schemas.Post.model_validate(post)
  #   # Update votes field using model_copy
  #   post_schema = post_schema.model_copy(update={"votes": vote_count or 0})
  #   posts.append(post_schema)
  
  #print(posts)
  return posts
  # return posts
  # print(posts)
  # return posts




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
  
  new_post = models.Post(     #it is used to retrieve all attributes(column) in DataBase table
    owner_id=current_user.id , **post.dict()
  )
  # print(current_user.id)
  # print(current_user.email)
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
@router.get("/{id}",response_model=schemas.PostOut)  #getting response from schemas.Post       
#id represents the path parameter id of specific post
def get_post(id:int,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):     #(response:Response)changing the response of the error occurred like 200 to 404    
  #automatically converts the the inbuilt string into int
  # cursor.execute("""SELECT * FROM posts where id=%s""",(str(id)))
  # post=cursor.fetchone()
  # post=db.query(models.Post).filter(models.Post.id == id).first()   #since we know that it contains only one post with unique id so instead of all() we can use first so one value is given
  
  post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() 
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
    
  # if post.owner_id != current_user.id:     restricts the view of ur data fro permitted owner_id only
  #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    # response.status_code=status.HTTP_404_NOT_FOUND   #changes the error code from 200 to 404  and inbuilt package provides the status of the error
    # return{'message':f"post with id: {id} was not found"}
  return post




     #DELETE THE POSTS
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)   #directly updating the status code by giving it in the decorator
def delete_post(id:int,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
  #deleting post
  #find the index of the array that has replaced ID
  #my_posts.pop(index)
  # cursor.execute("""DELETE FROM posts where id=%s returning *""",(str(id),))
  # deleted_post=cursor.fetchone()      #sql code
  # conn.commit()
  
  post_query=db.query(models.Post).filter(models.Post.id == id)   #we give conditions to delete post only when owner_id is equal
  
  post=post_query.first()
  
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
  
  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
  post_query.delete(synchronize_session=False)
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
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
  
  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
  
  post_query.update(post_data.model_dump(),synchronize_session=False)   #dict() is Pydantic v2 does ot work on sqlalchemy model
  
  db.commit()   #commit it to database
  
  return post_query.first() #after updating post and send it back to user    removed {"data":} because we just return only content not data
  