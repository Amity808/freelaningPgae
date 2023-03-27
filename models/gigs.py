from datetime import datetime

from sqlalchemy import Column, String, Float, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.users import Users

from .base_class import Base


class Gig(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(88), nullable=False)
    search_tags = Column(String(40), nullable=False)
    gig_description = Column(String(800), nullable=False)
    gig_requirements = Column(String(40), nullable=False)
    faq = Column(String)

    created_at = Column(String)
    is_active = Column(Boolean)

    users_id = Column(Integer, ForeignKey("users.id"))
    profile_id = Column(Integer, ForeignKey("profile.id"))
    request_id = Column(Integer, ForeignKey("request.id"))
    basic_package = Column(Integer, ForeignKey("basicpackage.id"))
    standard_package = Column(Integer, ForeignKey("standardpackage.id"))
    premium_package = Column(Integer, ForeignKey("premiumpackage.id"))

    users = relationship("Users", back_populates="gig")
    profile = relationship("Profile", back_populates="gig")
    basicpackage = relationship("Basicpackage", back_populates="gig")
    standardpackage = relationship("Standardpackage", back_populates="gig")
    premiumpackage = relationship("Premiumpackage", back_populates="gig")
    request = relationship("Request", back_populates="gig")


class Basicpackage(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    basic_description = Column(String, nullable=False)
    delivery_date = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    # gigs = Column(Integer, ForeignKey("gig.id"))
    users_id = Column(Integer, ForeignKey("users.id"))
    # gig_id = Column(Integer, ForeignKey("gig.id"))
    profile_id = Column(Integer, ForeignKey("profile.id"))

    users = relationship("Users", back_populates="basicpackage")
    gig = relationship("Gig", back_populates="basicpackage")
    profile = relationship("Profile", back_populates="basicpackage")


class Standardpackage(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    standard_description = Column(String, nullable=False)
    delivery_date = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    users_id = Column(Integer, ForeignKey("users.id"))
    # gig_id = Column(Integer, ForeignKey("gig.id"))
    profile_id = Column(Integer, ForeignKey("profile.id"))

    users = relationship("Users", back_populates="standardpackage")
    gig = relationship("Gig", back_populates="standardpackage")
    profile = relationship("Profile", back_populates="standardpackage")


class Premiumpackage(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    premium_description = Column(String, nullable=False)
    delivery_date = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    # gigs = Column(Integer, ForeignKey("gig.id"))
    users_id = Column(Integer, ForeignKey("users.id"))

    profile_id = Column(Integer, ForeignKey("profile.id"))

    users = relationship("Users", back_populates="premiumpackage")
    gig = relationship("Gig", back_populates="premiumpackage")
    profile = relationship("Profile", back_populates="premiumpackage")


class Request(Base):
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(150))
    price = Column(Integer)
    dilivery_date = Column(String)

    # gig_id = Column(Integer, ForeignKey("gig.id"))
    users_id = Column(Integer, ForeignKey("users.id"))
    # profile_id = Column(Integer, ForeignKey("profile.id"))

    users = relationship("Users", back_populates="request")
    gig = relationship("Gig", back_populates="request")
    profile = relationship("Profile", back_populates="request")


class Profile(Base):
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String)
    phone_no = Column(String, nullable=False)
    profileDescription = Column(String, nullable=False)
    school = Column(String, nullable=False)
    courseStudy = Column(String, nullable=False)
    certificate = Column(String, nullable=False)
    certifiedBy = Column(String, nullable=False)
    websiteUrl = Column(String, nullable=False)
    statusM = Column(String, nullable=False)
    # file_name = Column(String)

    users_id = Column(Integer, ForeignKey("users.id"))
    # gig_id = Column(Integer, ForeignKey("gig.id"))
    request_id = Column(Integer, ForeignKey("request.id"))

    gig = relationship("Gig", back_populates="profile")
    users = relationship("Users", back_populates="profile")
    basicpackage = relationship("Basicpackage", back_populates="profile")
    standardpackage = relationship("Standardpackage", back_populates="profile")
    premiumpackage = relationship("Premiumpackage", back_populates="profile")
    request = relationship("Request", back_populates="profile")


class ProfileImg(Base):
    id = Column(Integer, primary_key=True, index=True)
    picture = Column(String)

    users_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("Users", back_populates="profileimg")


class GigImage(Base):
    id = Column(Integer, primary_key=True, index=True)
    picture_one = Column(String)
    contentby = Column(String)

    picture_two = Column(String)
    file_name_two = Column(String)

    video_file = Column(String)
    video_name = Column(String)

    file_doc = Column(String)
    content_type = Column(String)

    users_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("Users", back_populates="gigimage")


class GigVideo(Base):
    id = Column(Integer, primary_key=True, index=True)
    gig_video = Column(String)
    video_name = Column(String)

    users_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("Users", back_populates="gigvideo")
