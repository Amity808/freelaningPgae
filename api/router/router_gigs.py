import os.path
import shutil
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from core.config import settings
from api.router.authentication import oauth2_scheme
from core import oauth
from core.token import get_current_user
from models.users import Users
from schemas.gigs import GigBase, GigRes
from models.gigs import Gig
from db.database import get_db
from api.repo.repo_gigs import (
    create_new_gig,
    list_allGig,
    retrieve_Gig_Id,
    delete_gigId,
)

router = APIRouter()


@router.post("/create-gig", response_model=GigRes)
def create_Gig(
        title: str = Form(...),
        search_tags: str = Form(...),
        gig_description: str = Form(...),
        gig_requirements: str = Form(...),
        faq: str = Form(...),
        is_active: bool = True,
        gig_doc: UploadFile = File(...),
        gig_video: UploadFile = File(...),
        gig_image: UploadFile = File(...),
        db: Session = Depends(get_db),
):
    filename = uuid.uuid4()

    extname = os.path.splitext(gig_image.filename)[1]
    gig_file_image = f"{filename}{extname}"

    extdocname = os.path.splitext(gig_doc.filename)[1]
    doc_file_name = f"{filename}{extdocname}"

    extvid_name = os.path.splitext(gig_video.filename)[1]
    gig_file_video = f"{filename}{extvid_name}"

    with open(f"static/gigimages/{gig_file_image}", "wb+") as buffer:
        shutil.copyfileobj(gig_image.file, buffer)

    with open(f"static/gigdocs/{doc_file_name}", "wb+") as buffer:
        shutil.copyfileobj(gig_doc.file, buffer)

    with open(f"static/gigvideos/{gig_file_video}", "wb+") as buffer:
        shutil.copyfileobj(gig_video.file, buffer)

    gigs = Gig(
        title=title,
        search_tags=search_tags,
        gig_description=gig_description,
        gig_requirements=gig_requirements,
        faq=faq,
        is_active=is_active,
        gig_doc=doc_file_name,
        gig_video=gig_file_video,
        gig_image=gig_file_image,
    )
    db.add(gigs)
    db.commit()
    db.refresh(gigs)
    return gigs


@router.post("/create-a-gig", response_model=GigRes)
def create_gig(
        gig: GigBase,
        db: Session = Depends(get_db),
        current_user: str = Depends(oauth.oauth2_scheme),
):
    user = get_current_user(db, current_user)
    users_id = user.id
    gigs = Gig(**gig.dict(), users_id=users_id)
    db.add(gigs)
    db.commit()
    db.refresh(gigs)
    return gigs


@router.get("/get-all-gig")
def get_all(db: Session = Depends(get_db)):
    gigs = list_allGig(db)
    return gigs


@router.get("/get-byId/{id}", response_model=GigRes)
def get_byId(id: int, db: Session = Depends(get_db)):
    gigs = retrieve_Gig_Id(id, db)
    return gigs


@router.get("/gig/autocomplete")
def autocompelete(terms: Optional[str], db: Session = Depends(get_db)):
    gigs = db.query(Gig).filter(Gig.title.contains(terms)).all()
    suggestions = []
    for gig in gigs:
        suggestions.append(gig.title)
    return suggestions


@router.put("/updateGig/{id}")
def updateId(
        id: int,
        gig: GigBase,
        db: Session = Depends(get_db),
        current_user=Depends(oauth.oauth2_scheme),
):
    users = get_current_user(db, current_user)
    existing_gigs = db.query(Gig).filter(Gig.id == id)
    if not existing_gigs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the {id} does not exist",
        )
    if existing_gigs.first().users_id == users.id:
        gig.__dict__.update(id=id)
        existing_gigs.update(gig.__dict__)
        db.commit()
        return {"message": "Successfully Updated"}
    else:
        return {"message": " Your are not authorized"}


@router.delete("/delete-gig/{id}")
def delete_gigs(
        id: int, db: Session = Depends(get_db), current_user=Depends(oauth.oauth2_scheme)
):
    user = get_current_user(db, current_user)
    existing_gigs = db.query(Gig).filter(Gig.id == id)
    if not existing_gigs.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} not found",
        )
    if existing_gigs.first().users_id == user.id:
        existing_gigs.delete(synchronize_session=False)
        db.commit()
        return {"message": f"Sucessfully deleted"}
    else:
        return {"message": "You are not Authorized"}
