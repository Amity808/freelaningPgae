from fastapi import APIRouter, Request, Depends, responses, status, HTTPException
from fastapi.templating import Jinja2Templates
from jose import jwt
from sqlalchemy.orm import Session

from db.database import get_db
from models.gigs import Profile
from models.users import Users

from core.config import settings

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/profile/{id}")
def profile_detail(request: Request, id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == id).first()
    errors = []
    if not profile:
        errors.append("Profile does not exist")
    return templates.TemplateResponse(
        "profile_details.html", {"request": request, "profile": profile, "errors": errors}
    )


@router.get("/update-profile/{id}")
def update_gig(id: int, request: Request, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == id).first()
    return templates.TemplateResponse("update_profile.html", {"request": request, "profile": profile})

@router.get("/profilecreate")
def create_gig(request: Request):
    return templates.TemplateResponse("profile_reg.html", {"request": request})


@router.post("/profilecreate")
async def create_gig(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    surname = form.get("surname")
    firstName = form.get("firstName")
    lastName = form.get("lastName")
    phone_no = form.get("phone_no")
    profileDescription = form.get("profileDescription")
    school = form.get("school")
    courseStudy = form.get("courseStudy")
    certificate = form.get("certificate")
    certifiedBy = form.get("certifiedBy")
    websiteUrl = form.get("websiteUrl")
    statusM = form.get("statusM")
    errors = []

    try:
        token = request.cookies.get("access_token")
        if token is None:
            errors.append("Not Authorized")
            return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
        else:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(param, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            email = payload.get("sub")
            users = db.query(Users).filter(Users.email == email).first()

            if users is None:
                errors.append("User does not exist, Kindly Register")
                return templates.TemplateResponse("user_register.html", {"request": request, "errors": errors})
            else:
                profiles = Profile(surname=surname, firstName=firstName,
                                   lastName=lastName, phone_no=phone_no,
                                   profileDescription=profileDescription,
                                   school=school, courseStudy=courseStudy,
                                   certificate=certificate, certifiedBy=certifiedBy,
                                   websiteUrl=websiteUrl, statusM=statusM)
                db.add(profiles)
                db.commit()
                db.refresh(profiles)
                return responses.RedirectResponse(f"/profile/{profiles.id}", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        errors.append("Kindly Contact Support Team bolarinwamuhdsodiq@gmail.com")
        return templates.TemplateResponse("profile_reg.html", {"request": request, "errors": errors})


