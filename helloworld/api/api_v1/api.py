from fastapi import APIRouter

from helloworld.api.api_v1.endpoints import (
    user
)

api_router = APIRouter()
api_router.include_router(user.router, tags=["user"])
