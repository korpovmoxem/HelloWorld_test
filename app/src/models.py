from typing import Optional
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator

"""
Для моделей определен минимальный набор атрибутов, необходимый для работы по ТЗ
"""

FILTER_CONDITIONS = [
    'eq',
    'lte',
    'gte'
]
FILTER_CONDITIONS_STR = ' | '.join(FILTER_CONDITIONS)


class InvalidFilterValue(ValueError):
    def __init__(self, message: str | None = None):
        if message is None:
            message = (f"Значение фильтра должно быть в формате: "
                       f"<тип сравнения ({FILTER_CONDITIONS_STR}'):числовое значение атрибута>")
        super().__init__(message)


class APIHeroPowerstats(BaseModel):
    intelligence: int
    strength: int
    speed: int
    power: int


class APIHero(BaseModel):
    id: int
    name: str
    full_name: str
    powerstats: APIHeroPowerstats


class GetHeroRequest(BaseModel):
    name: Optional[str] = None
    intelligence: Optional[str] = None
    strength: Optional[str] = None
    speed: Optional[str] = None
    power: Optional[str] = None

    @field_validator('intelligence', 'strength', 'speed', 'power')
    def validate_filter(cls, value):
        if value is None:
            return value

        if ':' not in value:
            raise InvalidFilterValue

        condition, val = value.split(':')
        if condition not in FILTER_CONDITIONS:
            raise InvalidFilterValue(f"Неверный тип сравнения. Допустимые: {FILTER_CONDITIONS_STR}")
        elif not val.isdigit():
            raise InvalidFilterValue(f"Значение после ':' должно быть типа int")
        return value


class GetHeroResponse(BaseModel):
    id: int
    external_id: int
    name: str
    full_name: str
    intelligence: int
    strength: int
    speed: int
    power: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)