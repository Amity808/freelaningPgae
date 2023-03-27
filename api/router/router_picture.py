import os.path
import shutil
import uuid
import secrets
# from PIL import Image
#
from fastapi import APIRouter, Depends, status, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session

from db.database import get_db
from models.gigs import ProfileImg

router = APIRouter()


@router.post("/profile-pictre-upload")
def create_upload_file(picture: UploadFile = File(...), db: Session = Depends(get_db)):

    filename = uuid.uuid4()
    extname = os.path.splitext(picture.filename)[1]
    profile_img_name = f"{filename}{extname}"

    with open(f"static/profileimg/{profile_img_name}", "wb+") as buffer:
        shutil.copyfileobj(picture.file, buffer)

    proimg = ProfileImg(picture=profile_img_name)
    db.add(proimg)
    db.commit()
    db.refresh(proimg)
    return proimg


@router.put("/profile-pictre-update/{id}")
def update_profilePicture(
    id: int, picture: UploadFile = File(None), db: Session = Depends(get_db)
):
    existing_picture = db.query(ProfileImg).filter(ProfileImg.id == id)

    if not existing_picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile Picture with the {id} does not exist",
        )

    if picture is not None:
        filename = uuid.uuid4()
        extname = os.path.splitext(picture.filename)[1]

        picture_img_name = f"{filename}{extname}"

        with open(f"static/profileimg/{picture_img_name}", "wb+") as buffer:
            shutil.copyfileobj(picture.file, buffer)

        os.remove(f"static/profileimg/{existing_picture}")

        existing_picture = picture_img_name

    picture_img_name.__dict__.update(id=id)
    existing_picture.update(picture_img_name.__dict__)
    db.commit()
    return {"Details": "Successfully Updated"}


@router.post("/uploadfile/profile")
async def create_upload_file(file: UploadFile = File(...)):
    FILEPATH = "static/profileimg/"
    filename = file.filename
    extenions = filename.split(".")[1]

    if extenions not in ["png", "jpg"]:
        return {"status": "error", "details": "file must be png or jpg"}

    token_name = secrets.token_hex(10) + "." + extenions
    generate_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generate_name, "wb") as file:
        file.write(file_content)

    img = Image
