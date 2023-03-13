from fastapi import APIRouter
from convergent.api.routes.base import base_router
from convergent.api.routes.public import public_router

root = APIRouter()
root.include_router(base_router)
root.include_router(public_router)
