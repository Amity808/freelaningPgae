from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from schemas.gigs import RequestBase, RequestRes
from models.gigs import Request


def create_new_request(request: RequestBase, db: Session, users_id: int):
    requests = Request(**request.dict(), users_id=users_id)
    db.add(requests)
    db.commit()
    db.refresh(requests)
    return requests


def list_AllRequest(db: Session):
    requests = db.query(Request).all()
    return requests


def retrieve_RequestId(id: int, db: Session):
    requests = db.query(Request).filter(Request.id == id).first()
    if not requests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The profile with the id {id} not found",
        )
    return requests


def update_RequestId(id: int, request: RequestBase, db: Session):
    existing_request = db.query(Request).filter(Request.id == id)
    if not existing_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The profile with the id {id} does not exist",
        )
    request.__dict__.update(id=id)
    existing_request.update(request.__dict__)
    db.commit()
    return existing_request


def delete_RequestId(id: int, db: Session):
    existing_request = db.query(Request).filter(Request.id == id)
    if not existing_request.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} does not exist",
        )
    existing_request.delete(synchronize_session=False)
    db.commit()
    return {"details": "Sucessfully Deleted"}
