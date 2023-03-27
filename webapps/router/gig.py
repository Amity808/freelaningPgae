from typing import Optional

from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from jose import jwt
from sqlalchemy.orm import Session
from datetime import datetime

from core.config import settings
from db.database import get_db
from models.gigs import Gig, GigImage
from models.users import Users

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def gig_home(request: Request, db: Session = Depends(get_db), msg: str = None):
    gigs = db.query(Gig).all()
    pic = db.query(GigImage).all()
    return templates.TemplateResponse(
        "gig_homepage.html", {"request": request, "gigs": gigs, "pic": pic, "msg": msg}
    )


@router.get("/details/{id}")
def git_detail(request: Request, id: int, db: Session = Depends(get_db)):
    gig = db.query(Gig).filter(Gig.id == id).first()
    user = db.query(Users).filter(Users.id == gig.users_id).first()
    return templates.TemplateResponse(
        "gig_detail.html", {"request": request, "gig": gig, "user": user}
    )


@router.get("/update-gig/{id}")
def update_gig(id: int, request: Request, db: Session = Depends(get_db)):
    gigs = db.query(Gig).filter(Gig.id == id).first()
    return templates.TemplateResponse("update_gig.html", {"request": request, "gigs": gigs})

@router.get("/create-gig")
def create_gig(request: Request):
    return templates.TemplateResponse("create_gig.html", {"request": request})


@router.post("/create-gig")
async def create_gig(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    title = form.get("title")
    search_tags = form.get("search_tags")
    gig_description = form.get("gig_description")
    gig_requirements = form.get("gig_requirements")
    faq = form.get("fags")
    errors = []
    if not title or len(title) < 2:
        errors.append("Title should be more than 10")
        return templates.TemplateResponse(
            "create_gig.html", {"request": request, "errors": errors}
        )
    if not gig_description or len(gig_description) < 10:
        errors.append("Description should be more than 10")
        return templates.TemplateResponse(
            "create_gig.html", {"request": request, "errors": errors}
        )
    try:
        token = request.cookies.get("access_token")
        if token is None:
            errors.append("Kindly Login first")
            return templates.TemplateResponse(
                "create_gig.html", {"request": request, "errors": errors}
            )
        else:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(
                param, settings.SECRET_KEY, algorithms=settings.ALGORITHM
            )
            email = payload.get("sub")
            users = db.query(Users).filter(Users.email == email).first()
            if users is None:
                errors.append(
                    "You are authenticated, Kindly Create account or Login to your existing account"
                )
                return templates.TemplateResponse(
                    "create_gig.html", {"request": request, "errors": errors}
                )
            else:
                gigs = Gig(
                    title=title,
                    search_tags=search_tags,
                    gig_description=gig_description,
                    gig_requirements=gig_requirements,
                    faq=faq,
                    created_at=datetime.now().date(),
                    users_id=users.id,
                )
                db.add(gigs)
                db.commit()
                db.refresh(gigs)
                return responses.RedirectResponse(
                    f"/details/{gigs.id}", status_code=status.HTTP_302_FOUND
                )
    except Exception as e:
        errors.append("Kindly contact us")
        return templates.TemplateResponse(
            "create_item.html", {"request": request, "errors": errors}
        )


@router.get("/update-delete-gig")
def delete_gig(request: Request, db: Session = Depends(get_db)):
    errors = []
    token = request.cookies.get("access_token")
    if token is None:
        errors.append("Kindly Login")
        return templates.TemplateResponse(
            "gig_update_delete.html", {"request": request, "errors": errors}
        )
    else:
        try:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(
                param, settings.SECRET_KEY, algorithms=settings.ALGORITHM
            )
            email = payload.get("sub")
            users = db.query(Users).filter(Users.email == email).first()
            gigs = db.query(Gig).filter(Gig.users_id == users.id).all()
            return templates.TemplateResponse(
                "gig_update_delete.html", {"request": request, "gigs": gigs, "users": users}
            )
        except Exception as e:
            errors.append("Somthing is wrong")
            print(e)
            return templates.TemplateResponse(
                "gig_update_delete.html", {"request": request, "errors": errors}
            )


@router.get("/search")
def search_button(request: Request, query: Optional[str], db: Session = Depends(get_db)):
    gigs = db.query(Gig).filter(Gig.title.contains(query)).all()
    return templates.TemplateResponse("gig_homepage.html", {"request": request, "gigs": gigs})




