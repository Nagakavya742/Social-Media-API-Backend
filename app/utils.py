from passlib.context import CryptContext
pwd_context=CryptContext(
  schemes=["bcrypt_sha256"],
  deprecated="auto"
  )    #here default hashing algo was bcrypt  bcrypt-sha256 supports any length password
#create engine all our models

def hash(password:str):
  return pwd_context.hash(password)
  