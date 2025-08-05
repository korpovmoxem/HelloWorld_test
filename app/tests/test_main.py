import json
import os

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


with open(f'{os.path.dirname(os.path.abspath(__file__))}{os.sep}test_cases.json', 'r', encoding='utf-8') as file:
    test_cases = json.load(file)


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client


@pytest.mark.anyio
@pytest.mark.parametrize(
    "case",
    test_cases['add_hero'],
    ids=lambda test: f"case-{test['params']}"
)
async def test_add_hero(async_client, case):
    response = await async_client.post('/hero/', params=case['params'])
    assert response.status_code == case['status']


@pytest.mark.anyio
@pytest.mark.parametrize(
    "case",
    test_cases['get_hero'],
    ids=lambda test: f"case-{test['params']}"
)
async def test_get_hero(async_client, case):
    response = await async_client.get('/hero/', params=case['params'])
    assert response.status_code == case['status']