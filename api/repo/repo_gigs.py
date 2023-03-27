from fastapi import HTTPException, status, UploadFile, Form, File
from sqlalchemy.orm import Session

from schemas.gigs import GigBase
from models.gigs import Gig


def create_new_gig(gig: GigBase, db: Session, users_id: int):
    gigs = Gig(**gig.dict(), users_id=users_id)
    db.add(gigs)
    db.commit()
    db.refresh(gigs)
    return gigs


def list_allGig(db: Session):
    gigs = db.query(Gig).filter().all()
    return gigs


def retrieve_Gig_Id(id: int, db: Session):
    gigs = db.query(Gig).filter(Gig.id == id).first()
    if not gigs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The id {id} with the details does not exist",
        )
    return gigs


def delete_gigId(id: int, db: Session):
    existing_gigs = db.query(Gig).filter(Gig.id == id)
    if not existing_gigs.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} not found",
        )
    existing_gigs.delete(synchronize_session=False)
    return {"details": f"Sucessfully deleted {existing_gigs}"}
