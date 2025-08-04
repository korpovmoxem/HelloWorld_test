from typing import Annotated

from fastapi import APIRouter, Query

from app.src.services import search_hero_request
from app.src.models import (
    AddHeroRequest,
)


router = APIRouter()


@router.post('/hero/')
async def add_hero(attrs: Annotated[AddHeroRequest, Query()]):
    return await search_hero_request(attrs.name)


