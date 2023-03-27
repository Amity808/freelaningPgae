from datetime import datetime

from sqlalchemy import Column, String, Float, Boolean, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from .base_class import Base


class Users(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(Date)

    profile = relationship("Profile", back_populates="users")
    gig = relationship("Gig", back_populates="users")
    basicpackage = relationship("Basicpackage", back_populates="users")
    standardpackage = relationship("Standardpackage", back_populates="users")
    premiumpackage = relationship("Premiumpackage", back_populates="users")
    request = relationship("Request", back_populates="users")
    profileimg = relationship("ProfileImg", back_populates="users")
    gigimage = relationship("GigImage", back_populates="users")
    gigvideo = relationship("GigVideo", back_populates="users")

