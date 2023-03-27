import os
import shutil
import uuid

from fastapi import HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from schemas.profile import ProfileBase, ProfileRes
from models.gigs import Profile


def create_new_profile(profile: ProfileBase, db: Session, users_id: int):
    profiles = Profile(**profile.dict(), users_id=users_id)
    db.add(profiles)
    db.commit()
    db.refresh(profiles)
    return profiles


def list_AllProfile(db: Session):
    profiles = db.query(Profile).all()
    return profiles


def retrieve_ProfileId(id: int, db: Session):
    profiles = db.query(Profile).filter(Profile.id == id).first()
    if not profiles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The profile with the id {id} not found",
        )
    return profiles


def update_ProfileId(id: int, profile: ProfileBase, db: Session):
    existing_profile = db.query(Profile).filter(Profile.id == id)
    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The profile with the id {id} does not exist",
        )
    profile.__dict__.update(id=id)
    existing_profile.update(profile.__dict__)
    db.commit()
    return existing_profile


def delete_ProfileId(id: int, db: Session):
    existing_price = db.query(Profile).filter(Profile.id == id)
    if not existing_price.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} does not exist",
        )
    existing_price.delete(synchronize_session=False)
    db.commit()
    return {"details": f"Sucessfully Deleted {existing_price}"}
