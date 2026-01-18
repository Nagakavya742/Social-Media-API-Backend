from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

#base is a Basemodel from a sqlalchemy  
class Post(Base):      #model 1
  __tablename__="posts"
  
  id = Column(Integer,primary_key=True,nullable=False)
  title=Column(String,nullable=False)
  content=Column(String,nullable=False)
  published=Column(Boolean,server_default='TRUE',nullable=False)
  created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
  owner_id=Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
  
  owner=relationship("User")   #building a relationship b/w owner and user
     

class User(Base):
  __tablename__="users"
  id = Column(Integer,primary_key=True,nullable=False)
  email = Column(String,nullable=False,unique=True)
  password = Column(String,nullable=False)
  created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
  phone_number=Column(String)      # it does not set up new column in post table it  is drawback of sqlalchemy


class Vote(Base):
  __tablename__="votes"
  user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
  post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)