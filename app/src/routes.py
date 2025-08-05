from fastapi import APIRouter, HTTPException, Query
from fastapi.params import Depends, Annotated
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.models import APIHero, GetHeroRequest, GetHeroResponse
from app.src.database import Hero
from app.src.utils.database_funcs import get_session
from app.src.utils.external_api import search_hero_request


router = APIRouter(tags=['superhero'])


@router.post('/hero/')
async def add_hero(
        name: str,
        single_mode: bool = False,
        session: AsyncSession = Depends(get_session)
) -> str:
    """
    Поиск героя на SuperHeroAPI и запись в БД, если найденный герой не записан
    - **name**: Имя героя
    - **single_mode**: Режим поиска героя. Если True, то при нахождении более одного героя по имени будет вызвана ошибка
    """
    result = await search_hero_request(name)

    if result['response'] == 'error':
        match result['error']:
            case 'character with given name not found':
                raise HTTPException(
                    status_code=404,
                    detail=f"Герой с именем '{name}' не найден"
                )
    heroes = result['results']

    # Проверка при single_mode=True
    if single_mode and len(heroes) > 1:
        raise HTTPException(
            status_code=400,
            detail=f"По запросу '{name}' найдено более одного героя"
        )

    # Валидация результатов запроса
    hero_models = [APIHero(**hero, full_name=hero['biography']['full-name']) for hero in heroes]

    # Проверка на уже записанных героев в БД
    query = (
        select(Hero.name)
        .where(
            Hero.name not in [hero_model.name for hero_model in hero_models],
            Hero.full_name not in [hero_model.full_name for hero_model in hero_models],
        )
    )
    rows = await session.execute(query)
    existing_hero_names = rows.scalars().all()
    new_heroes = list(filter(lambda hero: hero.name not in existing_hero_names, hero_models))

    # Запись новых героев
    new_hero_rows = [
        Hero(
            name=item.name,
            full_name=item.full_name,
            external_id=item.id,
            **item.powerstats.model_dump()
        ) for item in new_heroes
    ]
    session.add_all(new_hero_rows)
    await session.commit()

    return f'Добавлено новых героев: {len(new_hero_rows)}'


@router.get('/hero/', response_model=list[GetHeroResponse])
async def get_hero(
        hero_filter: Annotated[GetHeroRequest, Query()],
        session: AsyncSession = Depends(get_session)
):
    """
    Получить героев по фильтрам
    - **name**: Имя героя. По данному фильтру ищется полное совпадение

    Следующие параметры должны быть переданы в формате **<тип сравнения>:<числовое значение>**:
    - **intelligence**
    - **strength**
    - **speed**
    - **power**

    Допустимые типы сравнения:
    - **eq**: Атрибут героя должен быть равен переданному значение (==)
    - **lte**: Атрибут героя должен быть меньше или равен переданному значение (<=)
    - **gte**: Атрибут героя должен быть больше или равен переданному значению (>=)

    Пример корректно переданного значения фильтра: <code>speed=gte:96</code>
    """

    conditions = []

    # Форматирование переданных атрибутов из строк в атрибуты ORM
    for field, value in hero_filter.model_dump(exclude_unset=True).items():
        if field == 'name':
            conditions.append(func.lower(Hero.name) == value.lower())
        else:
            cond_type, cond_value = value.split(':')
            sql_attr = getattr(Hero, field, None)
            match cond_type:
                case 'eq':
                    conditions.append(sql_attr == cond_value)
                case 'lte':
                    conditions.append(sql_attr <= cond_value)
                case 'gte':
                    conditions.append(sql_attr >= cond_value)

    query = select(Hero).where(and_(*conditions))
    rows = await session.execute(query)
    rows = rows.scalars().all()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail='По переданным фильтрам не найдено ни одного героя'
        )
    return [GetHeroResponse.model_validate(row) for row in rows]