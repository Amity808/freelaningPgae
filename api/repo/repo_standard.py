from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from schemas.gigs import StandardBase, StandardRes
from models.gigs import Standardpackage


def create_new_standard(standard: StandardBase, db: Session, users_id: int):
    standards = Standardpackage(**standard.dict(), users_id=users_id)
    db.add(standards)
    db.commit()
    db.refresh(standards)
    return standards


def list_AllStandard(db: Session):
    price = db.query(Standardpackage).all()
    return price


def retrieve_standardId(id: int, db: Session):
    price = db.query(Standardpackage).filter(Standardpackage.id == id).first()
    if not price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The price package with the id {id} not found",
        )
    return price


def update_standardId(id: int, standard: StandardBase, db: Session):
    existing_price = db.query(Standardpackage).filter(Standardpackage.id == id)
    if not existing_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} does not exist",
        )
    standard.__dict__.update(id=id)
    existing_price.update(standard.__dict__)
    db.commit()
    return existing_price


def delete_standardId(id: int, db: Session):
    existing_price = db.query(Standardpackage).filter(Standardpackage.id == id)
    if not existing_price.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} does not exist",
        )
    existing_price.delete(synchronize_session=False)
    db.commit()
    return {"details": f"Sucessfully Deleted {existing_price}"}
