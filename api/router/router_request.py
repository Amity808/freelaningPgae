from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from core import oauth
from schemas.gigs import RequestBase, RequestRes
from models.gigs import Request
from db.database import get_db
from core.token import get_current_user
from core.oauth import oauth2_scheme
from api.repo.repo_request import (
    create_new_request,
    list_AllRequest,
    retrieve_RequestId,
    update_RequestId,
    delete_RequestId,
)


router = APIRouter()


@router.post("/create-request")
def create_Request(
    request: RequestBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2_scheme),
):
    users = get_current_user(db, current_user)
    users_id = users.id
    requests = create_new_request(request, db, users_id=users_id)
    return requests


@router.get("/get-allrequest")
def all_request(db: Session = Depends(get_db)):
    requests = list_AllRequest(db)
    return requests


@router.get("/get-request/{id}")
def requestId(
    id: int, db: Session = Depends(get_db), current_user=Depends(oauth.oauth2_scheme)
):
    requests = retrieve_RequestId(id, db)
    return requests


@router.put("/request/{id}")
def updateId(
    id: int,
    request: RequestBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.oauth2_scheme),
):
    users = get_current_user(db, current_user)
    existing_request = db.query(Request).filter(Request.id == id)
    if not existing_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The profile with the id {id} does not exist",
        )
    if existing_request.first().user_id == users.id:
        request.__dict__.update(id=id)
        existing_request.update(request.__dict__)
        db.commit()
        return existing_request
    else:
        return {"Details": "Not authorized"}


@router.delete("/request/{id}")
def delete_Id(
    id: int, db: Session = Depends(get_db), current_user=Depends(oauth.get_current_user)
):
    users = get_current_user(db, current_user)
    existing_request = db.query(Request).filter(Request.id == id)
    if not existing_request.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} does not exist",
        )
    if existing_request.first().user_id == users.id:
        existing_request.delete(synchronize_session=False)
        db.commit()
        return {"details": "Sucessfully Deleted"}
    else:
        return {"Details": "Not Authorized"}
