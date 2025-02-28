from jose import JWTError, jwt
from datetime import datetime, timedelta


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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt