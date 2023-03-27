from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File


class ProfileBase(BaseModel):
    surname: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phone_no: Optional[str] = None
    profileDescription: Optional[str] = None
    school: Optional[str] = None
    courseStudy: Optional[str] = None
    certificate: Optional[str] = None
    certifiedBy: Optional[str] = None
    websiteUrl: Optional[str] = None
    statusM: Optional[str] = None


class ProfileRes(ProfileBase):
    class Config:
        orm_mode = True


class ProfilePicture(BaseModel):
    picture: str
