import aiohttp

from app.config import settings


async def search_hero_request(name: str) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.get_superhero_api_url() + '/search/' + name) as response:
            print(response.status)

