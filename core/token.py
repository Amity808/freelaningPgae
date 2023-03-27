from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt


from models.users import Users
from schemas import users
from core.config import settings


ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encode_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = users.TokenData(email=email)
    except JWTError:
        raise credentials_exception


def get_current_user(db, current_user):
    try:
        payload = jwt.decode(
            current_user, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to Verify Credentials",
            )
        user = db.query(Users).filter(Users.email == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify Credent"
        )

    return user
