from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jose import jwt

from core.hashing import Hash
from db.database import get_db
from models.users import Users
from core.config import settings

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/login")
def login(request: Request, msg: str = None):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, response: Response, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("username")
    password = form.get("password")
    errors = []

    if not email:
        errors.append("Please Enter Valid Email")

    if not password or len(password) < 5:
        errors.append("Password should be more than 5 Enter a valid password")
    try:
        user = (
            db.query(Users).filter(Users.email == email).first()
            or db.query(Users).filter(Users.username == email).first()
        )
        if user is None:
            errors.append("Email does not exist")
            return templates.TemplateResponse(
                "login.html", {"request": request, "errors": errors}
            )
        else:
            if Hash.verify(password, user.password):
                data = {"sub": user.email}
                jwt_token = jwt.encode(
                    data, settings.SECRET_KEY, algorithm=settings.ALGORITHM
                )
                msg = "Login Successful"
                response = templates.TemplateResponse(
                    "login.html", {"request": request, "msg": msg}
                )
                response.set_cookie(
                    key="access_token", value=f"Bearer {jwt_token}", httponly=True
                )
                return response
            else:
                errors.append("Invalid Password")
                return templates.TemplateResponse(
                    "login.html", {"request": request, "errors": errors}
                )
    except:
        errors.append("Something went wrong")
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
