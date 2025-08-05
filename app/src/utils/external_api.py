import aiohttp

from app.config import settings


async def search_hero_request(name: str) -> dict:
    """
    Запрос к сервису SuperHero API для получения героя по имени
    При нескольких совпадениях по имени сервис возвращает всех найденных героев
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.get_superhero_api_url() + '/search/' + name, ssl=False) as response:
            result = await response.json()
            return result