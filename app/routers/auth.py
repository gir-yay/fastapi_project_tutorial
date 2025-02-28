from fastapi import Depends, APIRouter, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=["Authentication"],
)

router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={ "user_id": user.id })
    return { "access_token": access_token, "token_type": "bearer" }

