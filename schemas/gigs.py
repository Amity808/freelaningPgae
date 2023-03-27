from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date


class GigBase(BaseModel):
    title: str
    search_tags: str
    gig_description: str
    gig_requirements: str
    faq: str
    created_at: Optional[date] = datetime.now().date()
    is_active: bool = True


class GigRes(GigBase):
    class Config:
        orm_mode = True


class BasicBase(BaseModel):
    title: str
    basic_description: str
    delivery_date: Optional[date] = datetime.now().date()
    price: int


class BasicRes(BasicBase):
    class Config:
        orm_mode = True


class StandardBase(BaseModel):
    title: str
    standard_description: str
    delivery_date: Optional[date] = datetime.now().date()
    price: int


class StandardRes(BasicBase):
    class Config:
        orm_mode = True


class PremiumBase(BaseModel):
    title: str
    premium_description: str
    delivery_date: Optional[date] = datetime.now().date()
    price: int


class PremiumRes(PremiumBase):
    class Config:
        orm_mode = True


class RequestBase(BaseModel):
    description: str
    price: str
    dilivery_date: Optional[date] = datetime.now().date()


class RequestRes(RequestBase):
    class Config:
        orm_mode = True
