from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from core import oauth
from core.token import get_current_user
from models.gigs import Premiumpackage
from schemas.gigs import PremiumBase, PremiumRes

from db.database import get_db
from api.repo.repo_premium import (
    create_new_premium,
    list_AllPremium,
    retrieve_PremiumId,
)


router = APIRouter()


@router.post("/create-premiumprice")
def create_PremiumPrice(
    premium: PremiumBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.oauth2_scheme),
):
    users = get_current_user(db, current_user)
    users_id = users.id
    price = create_new_premium(premium, db, users_id=users_id)
    return price


@router.get("/get-all-premiumprice")
def all_premiumprice(db: Session = Depends(get_db)):
    price = list_AllPremium(db)
    return price


@router.get("/standardprice/{id}")
def premiumId(
    id: int, db: Session = Depends(get_db), current_user=Depends(oauth.get_current_user)
):
    price = retrieve_PremiumId(id, db)
    return price


@router.put("/premiumprice/{id}")
def updateId(
    id: int,
    premium: PremiumBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.get_current_user),
):
    users = get_current_user(db, current_user)
    existing_price = db.query(Premiumpackage).filter(Premiumpackage.id == id)
    if not existing_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} does not exist",
        )
    if existing_price.first().user_id == users.id:
        premium.__dict__.update(id=id)
        existing_price.update(premium.__dict__)
        db.commit()
        return existing_price
    else:
        return {"Details": "Not authenticated"}


@router.delete("/premiumprice/{id}")
def delete_Id(
    id: int, db: Session = Depends(get_db), current_user=Depends(oauth.get_current_user)
):
    users = get_current_user(db, current_user)
    existing_price = db.query(Premiumpackage).filter(Premiumpackage.id == id)
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
        return {"Detail": "Not authenticated"}
