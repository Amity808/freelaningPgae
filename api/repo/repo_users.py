from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from schemas.users import UserCreate, UserRes
from models.users import Users
from core.hashing import Hash


def create_new_user(user: UserCreate, db: Session):
    users = Users(
        username=user.username,
        email=user.email,
        password=Hash.bcrypt(user.password),
        created_at=user.created_at,
    )
    db.add(users)
    db.commit()
    db.refresh(users)
    return users


def list_AllUser(db: Session):
    users = db.query(Users).all()
    return users


def retrieve_UserId(id: int, db: Session):
    users = db.query(Users).filter(Users.id == id).first()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The profile with the id {id} not found",
        )
    return users


def update_UserId(id: int, user: UserCreate, db: Session):
    existing_user = db.query(Users).filter(Users.id == id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The profile with the id {id} does not exist",
        )
    user.__dict__.update(id=id)
    existing_user.update(user.__dict__)
    db.commit()
    return existing_user


def delete_UserId(id: int, db: Session):
    existing_user = db.query(Users).filter(Users.id == id)
    if not existing_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The details with the id {id} does not exist",
        )
    existing_user.delete(synchronize_session=False)
    db.commit()
    return {"details": "Sucessfully Deleted"}
