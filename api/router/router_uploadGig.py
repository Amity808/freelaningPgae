import os.path
import shutil
import uuid
import secrets
# from PIL import Image

from fastapi import APIRouter, Depends, status, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session
from core.token import get_current_user
from core.oauth import oauth2_scheme
from db.database import get_db
from models.gigs import GigImage

router = APIRouter()


@router.post("/gig-image-upload")
def create_upload_file(
    picture_one: UploadFile = File(...),
    picture_two: UploadFile = File(...),
    video_file: UploadFile = File(...),
    file_doc: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename = uuid.uuid4()

    extname = os.path.splitext(picture_one.filename)[1]
    picture_one_image = f"{filename}{extname}"

    extpicame = os.path.splitext(picture_two.filename)[1]
    picture_two_name = f"{filename}{extpicame}"

    extvid_name = os.path.splitext(video_file.filename)[1]
    video_file_name = f"{filename}{extvid_name}"

    extdocname = os.path.splitext(file_doc.filename)[1]
    file_doc_name = f"{filename}{extdocname}"

    with open(f"static/gigimages/{picture_one_image}", "wb+") as buffer:
        shutil.copyfileobj(picture_one.file, buffer)

    with open(f"static/gigimages/{picture_two_name}", "wb+") as buffer:
        shutil.copyfileobj(picture_two.file, buffer)

    with open(f"static/gigvideos/{video_file_name}", "wb+") as buffer:
        shutil.copyfileobj(video_file.file, buffer)

    gig = GigImage(
        picture_one=picture_one_image,
        contentby=picture_one.content_type,
        picture_two=picture_two_name,
        file_name_two=picture_two.content_type,
        file_doc=file_doc_name,
        content_type=file_doc.content_type,
        video_file=video_file_name,
        video_name=video_file.content_type,
    )

    db.add(gig)
    db.commit()
    db.refresh(gig)
    return gig


@router.get("/get-allimages")
def all_images(db: Session = Depends(get_db)):
    pic = db.query(GigImage).all()
    return pic


@router.put("/gig-image-update/{id}")
def update_image(
    id: int,
    picture_one: UploadFile = File(None),
    picture_two: UploadFile = File(None),
    video_file: UploadFile = File(None),
    file_doc: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    existing_gig = db.query(GigImage).filter(GigImage.id == id)
    if not existing_gig:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The id with {id} does not exist",
        )

    filename = uuid.uuid4()

    extname = os.path.splitext(picture_one.filename)[1]
    picture_one_image = f"{filename}{extname}"

    extpicame = os.path.splitext(picture_two.filename)[1]
    picture_two_name = f"{filename}{extpicame}"

    extvid_name = os.path.splitext(video_file.filename)[1]
    video_file_name = f"{filename}{extvid_name}"

    extdocname = os.path.splitext(file_doc.filename)[1]
    file_doc_name = f"{filename}{extdocname}"

    with open(f"static/gigimages/{picture_one_image}", "wb+") as buffer:
        shutil.copyfileobj(picture_one.file, buffer)

    os.remove(f"static/gigimages/{existing_gig.contentby}")

    with open(f"static/gigimages/{picture_two_name}", "wb+") as buffer:
        shutil.copyfileobj(picture_two.file, buffer)

    os.remove(f"static/gigimages/{existing_gig.file_name_two}")

    with open(f"static/gigvideos/{video_file_name}", "wb+") as buffer:
        shutil.copyfileobj(video_file.file, buffer)

    os.remove(f"static/gigimages/{existing_gig.content_type}")

    gig = GigImage(
        picture_one=picture_one_image,
        contentby=picture_one.content_type,
        picture_two=picture_two_name,
        file_name_two=picture_two.content_type,
        file_doc=file_doc_name,
        content_type=file_doc.content_type,
        video_file=video_file_name,
        video_name=video_file.content_type,
    )

    db.add(gig)
    db.commit()
    db.refresh(gig)
    return gig
