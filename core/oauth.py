from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import token
from .utils import OAuth2PasswordBearerWithCookie

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login/token")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authentication": "Bearer"},
    )

    return token.verify_token(data, credentials_exception)
