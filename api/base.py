from fastapi import APIRouter
from .router import (
    router_gigs,
    router_price,
    router_standard,
    router_premium,
    router_profile,
    router_request,
    router_users,
    authentication,
    router_picture,
    router_uploadGig,
)

from webapps.router import gig as web_gig, users as web_user, auth as web_auth
from webapps.router import profile as web_profile


api_router = APIRouter()

api_router.include_router(authentication.router, prefix="/login/token", tags=["Login"])
api_router.include_router(router_users.router, prefix="/user", tags=["User"])
api_router.include_router(router_gigs.router, prefix="/gigs", tags=["Gigs"])
api_router.include_router(router_price.router, prefix="/basic", tags=["Prices"])
api_router.include_router(router_standard.router, prefix="/standard", tags=["Standard"])
api_router.include_router(router_premium.router, prefix="/premium", tags=["Premium"])
api_router.include_router(router_profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(router_request.router, prefix="/request", tags=["Request"])
api_router.include_router(router_picture.router)
api_router.include_router(router_uploadGig.router)
api_router.include_router(web_gig.router)
api_router.include_router(web_user.router)
api_router.include_router(web_auth.router)
api_router.include_router(web_profile.router)
