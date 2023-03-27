from fastapi import APIRouter, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from core import token
from core.utils import OAuth2PasswordBearerWithCookie
from db.database import get_db
from models.users import Users
from schemas import users
from core.hashing import Hash
from core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login/token")


@router.post("", response_model=users.Token)
def login(response: Response,
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(Users).filter(Users.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Username"
        )
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inavlid Password provided"
        )
    data = {"sub": request.username}
    jwt_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True)
    return {"access_token": jwt_token, "token_type": "bearer"}
