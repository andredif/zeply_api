from fastapi import APIRouter

from . import addresses


api_router = APIRouter(prefix="/v1")

api_router.include_router(addresses.router)
