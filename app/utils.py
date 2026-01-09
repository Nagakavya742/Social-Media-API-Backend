from passlib.context import CryptContext
pwd_context=CryptContext(
  schemes=["bcrypt_sha256"],
  deprecated="auto"
  )    #here default hashing algo was bcrypt  bcrypt-sha256 supports any length password
#create engine all our models

def hash(password:str):
  return pwd_context.hash(password)
  
  
#converts the raw password into hash and compares the previous or first given password that converted into hash and compares both
def verify(plain_password,hashed_password):
  return pwd_context.verify(plain_password,hashed_password)   #called the hashing conversion function to convert and compare