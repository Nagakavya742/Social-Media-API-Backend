# from jose import JWTError,jwt
# from datetime import datetime,timedelta
# from . import schemas
# from fastapi import Depends,HTTPException,status
# from fastapi.security import OAuth2PasswordBearer

# oauth2_schema=OAuth2PasswordBearer(tokenUrl='/login')
# #SECRET_KEY
# #Algorithm
# #Expiration time

# SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6c"
# ALGORITHM="HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES=30

# def create_access_token(data:dict):
#   to_encode=data.copy()
#   expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#   to_encode.update({'exp':expire})
  
#   encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
  
#   return encode_jwt

# def verify_access_token(token:str,credentials_exception):
#   try:
#     payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
#     id=payload.get("user_id")
  
#     if id is None:
#       raise credentials_exception
#     token_data=schemas.TokenData(id=id)
    
#   except JWTError:
#     raise credentials_exception

#   return token_data
    
# def get_current_user(token:str=Depends(oauth2_schema)):    #verifies the token is correct and if it is it will get data from db and give it user
#   credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",headers={"www-Authentication": "Bearer"},)
#   return verify_access_token(token,credentials_exception)



from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# IMPORTANT: this must match your actual /login route path
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    # use UTC always
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # FIXED BUG HERE (you had id.str)
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data=schemas.TokenData(id=str(user_id))

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),db:Session=Depends(database.get_db)):   #when the given token is verified by verify_access_token the data from db is fetched and provided
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token=verify_access_token(token, credentials_exception)
    
    user=db.query(models.User).filter(models.User.id==token.id).first()
    
    return user
