from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.token import get_current_user
from schemas.gigs import PremiumBase, PremiumRes
from models.gigs import Premiumpackage


def create_new_premium(premium: PremiumBase, db: Session, users_id: int):
    price = Premiumpackage(**premium.dict(), users_id=users_id)
    db.add(price)
    db.commit()
    db.refresh(price)
    return price


def list_AllPremium(db: Session):
    price = db.query(Premiumpackage).all()
    return price


def retrieve_PremiumId(id: int, db: Session):
    price = db.query(Premiumpackage).filter(Premiumpackage.id == id).first()
    if not price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The price package with the id {id} not found",
        )
    return price
