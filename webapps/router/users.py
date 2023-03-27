from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.hashing import Hash
from db.database import get_db
from models.users import Users

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/register")
def registration(request: Request):
    return templates.TemplateResponse("user_register.html", {"request": request})


@router.post("/register")
async def registration(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    username = form.get("username")
    password = form.get("password")
    errors = []

    if len(password) < 6:
        errors.append("Password should be more than 6 character")
        return templates.TemplateResponse(
            "user_register.html", {"request": request, "errors": errors}
        )

    user = Users(email=email, username=username, password=Hash.bcrypt(password))
    try:

        db.add(user)
        db.commit()
        db.refresh(user)
        return responses.RedirectResponse(
            "/login?msg=Successfully Register", status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        errors.append("Email or Username already exist")
        return templates.TemplateResponse(
            "user_register.html", {"request": request, "errors": errors}
        )
