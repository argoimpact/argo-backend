from httpx import AsyncClient
import pytest
from starlette.status import HTTP_200_OK

import logging

from app.main import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@pytest.mark.anyio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == HTTP_200_OK
        assert response.json() == {"Hello": "World!"}


@pytest.mark.anyio
def test_config():
    from app.config import AppConfig

    app_config = AppConfig()
    assert app_config.openai_api_key
