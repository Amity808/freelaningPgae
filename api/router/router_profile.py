import os
import shutil
import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from core import oauth
from models.gigs import Profile
from schemas.profile import ProfileBase, ProfileRes

from db.database import get_db
from api.repo.repo_profile import (
    create_new_profile,
    retrieve_ProfileId,
    list_AllProfile,
    update_ProfileId,
    delete_ProfileId,
)
from core.oauth import oauth2_scheme
from core.token import get_current_user

router = APIRouter()


@router.post("/create-profile")
def create_profile(
    profile: ProfileBase,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2_scheme),
):
    users = get_current_user(db, current_user)
    users_id = users.id
    profiles = create_new_profile(profile, db, users_id)
    return profiles


@router.get("/get-all-profile")
def all_profile(db: Session = Depends(get_db)):
    profiles = list_AllProfile(db)
    return profiles


@router.get("/get-profile/{id}")
def standardId(id: int, db: Session = Depends(get_db)):
    profiles = retrieve_ProfileId(id, db)
    return profiles


@router.put("/updateprofile/{id}")
def updateId(
    id: int,
    profile: ProfileBase,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2_scheme),
):
    users = get_current_user(db, current_user)
    existing_profile = db.query(Profile).filter(Profile.id == id)
    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The profile with the id {id} does not exist",
        )
    if existing_profile.first().user_id == users.id:
        profile.__dict__.update(id=id)
        existing_profile.update(profile.__dict__)
        db.commit()
        return {"message": "Successfully updated"}
    else:
        return {"message": "Not Authentication"}


@router.delete("/delete-profile/{id}")
def delete_Id(
    id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2_scheme)
):
    users = get_current_user(db, current_user)
    existing_price = db.query(Profile).filter(Profile.id == id)
    if not existing_price.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} does not exist",
        )
    if existing_price.first().user_id == users.id:
        existing_price.delete(synchronize_session=False)
        db.commit()
        return {"details": f"Sucessfully Deleted {existing_price}"}
    else:
        return {"Details": "Not Authenticated"}
