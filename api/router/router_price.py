from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from core import oauth
from schemas.gigs import BasicBase, BasicRes
from models.gigs import Basicpackage
from db.database import get_db
from core.token import get_current_user
from api.repo.repo_price import create_new_basic, list_AllBasic, retrieve_GigId


router = APIRouter()


@router.post("/create-basicprice")
def create_BasicPrice(
    basic: BasicBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.get_current_user),
):
    users_id = get_current_user(db, current_user)
    price = create_new_basic(basic, db, users_id=users_id)
    return price


@router.get("/get-allBasicPrice")
def all_basicprice(db: Session = Depends(get_db)):
    price = list_AllBasic(db)
    return price


@router.get("/basicprice/{id}")
def basicId(
    id: int, db: Session = Depends(get_db), current_user=Depends(oauth.get_current_user)
):
    price = retrieve_GigId(id, db)
    return price


@router.put("/basicprice/{id}")
def updateId(
    id: int,
    basic: BasicBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.get_current_user),
):
    users = get_current_user(db, current_user)
    existing_price = db.query(Basicpackage).filter(Basicpackage.id == id)
    if not existing_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} does not exist",
        )
    if existing_price.first().user_id == users.id:
        basic.__dict__.update(id=id)
        existing_price.update(basic.__dict__)
        db.commit()
        return existing_price
    else:
        return {"Details": "Not Authenticted"}


@router.delete("/basicprice/{id}")
def delete_Id(
    id: int, db: Session = Depends(get_db), current_user=Depends(oauth.get_current_user)
):
    users = get_current_user(db, current_user)
    existing_price = db.query(Basicpackage).filter(Basicpackage.id == id)
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
