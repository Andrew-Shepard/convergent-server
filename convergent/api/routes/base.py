from enum import Enum
from typing import Optional, Union, List
from fastapi import APIRouter

base_router = APIRouter()
base_tags: Optional[List[Union[str, Enum]]] = ["base"]


@base_router.get("/health", tags=base_tags)
async def health():
    return {"status": "OK"}


@base_router.get("/info", tags=base_tags)
async def info():
    return {}
