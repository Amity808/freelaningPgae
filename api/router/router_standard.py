from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from core import oauth
from models.gigs import Standardpackage
from schemas.gigs import StandardBase, StandardRes
from core.token import get_current_user
from core.oauth import oauth2_scheme

from db.database import get_db
from api.repo.repo_standard import (
    create_new_standard,
    list_AllStandard,
    retrieve_standardId,
    update_standardId,
    delete_standardId,
)


router = APIRouter()


@router.post("/create-StandardPrice")
def create_StandardPrice(
    standard: StandardBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.oauth2_scheme),
):
    users = get_current_user(db, current_user)
    users_id = users.id
    price = create_new_standard(standard, db, users_id=users_id)
    return price


@router.get("/get-allStandardPrice")
def all_standardprice(db: Session = Depends(get_db)):
    price = list_AllStandard(db)
    return price


@router.get("/standardprice/{id}")
def standardId(
    id: int, db: Session = Depends(get_db), current_user=Depends(oauth.get_current_user)
):
    price = retrieve_standardId(id, db)
    return price


@router.put("/standardprice/{id}")
def updateId(
    id: int,
    standard: StandardBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.get_current_user),
):
    users = get_current_user(db, current_user)
    existing_price = db.query(Standardpackage).filter(Standardpackage.id == id)
    if not existing_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} does not exist",
        )
    if existing_price.first().user_id == users.id:
        standard.__dict__.update(id=id)
        existing_price.update(standard.__dict__)
        db.commit()
        return existing_price
    else:
        return {"Details": "Not Authenticated"}


@router.delete("/standardprice/{id}")
def delete_Id(
    id: int, db: Session = Depends(get_db), current_user=Depends(oauth.get_current_user)
):
    users = get_current_user(db, current_user)
    existing_price = db.query(Standardpackage).filter(Standardpackage.id == id)
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
        return {"Details": "Not Authentication"}
