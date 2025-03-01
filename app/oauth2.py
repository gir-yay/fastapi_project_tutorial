from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key to sign the JWT token
SECRET_KEY = "d33jkl2550po4kigt8tryr87urh556eu526ei"

# Algorithm used to sign the JWT token
ALGORITHM = "HS256"

# Expiration time for the JWT token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithms=[ALGORITHM])
    return encoded_jwt



def verify_jwt_token(token: str , credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id : str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise credentials_exception
    
def get_current_user(token : str = Depends(oauth2_scheme)):
    credientials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_jwt_token(token, credientials_exception)