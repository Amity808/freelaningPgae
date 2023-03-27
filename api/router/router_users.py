from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.users import UserCreate, UserRes

from db.database import get_db
from api.repo.repo_users import (
    create_new_user,
    list_AllUser,
    retrieve_UserId,
    update_UserId,
    delete_UserId,
)


router = APIRouter()


@router.post("/create-user", response_model=UserRes)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    users = create_new_user(user, db)
    return users


@router.get("/get-user")
def all_request(db: Session = Depends(get_db)):
    users = list_AllUser(db)
    return users


@router.get("/get-user/{id}", response_model=UserRes)
def userId(id: int, db: Session = Depends(get_db)):
    users = retrieve_UserId(id, db)
    return users


@router.put("/update-user/{id}")
def updateId(id: int, user: UserCreate, db: Session = Depends(get_db)):
    users = update_UserId(id, user, db)
    return {"Details": "Successfully update the details with the id {id}"}


@router.delete("/delete/{id}")
def delete_Id(id: int, db: Session = Depends(get_db)):
    users = delete_UserId(id, db)
    return {"details": f"Suceessfully deleted"}
