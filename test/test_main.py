from httpx import AsyncClient
import pytest
from fastapi import FastAPI
from starlette.status import HTTP_200_OK

from app.main import app  # Adjust the import path according to your project structure


@pytest.mark.anyio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == HTTP_200_OK
        assert response.json() == {"Hello": "World!"}
