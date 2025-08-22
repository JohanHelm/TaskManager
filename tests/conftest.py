from fastapi.testclient import TestClient
import pytest
import pytest_asyncio
from httpx import AsyncClient

from main import app
from fake_db.fake_dao import get_task_dao

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(base_url="http://127.0.0.1:8155") as client:
        yield client


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope="function")
def first_task():
    task_dao = get_task_dao()
    first_task = task_dao.get_pack(0, 1)
    return first_task[0]


@pytest.fixture
def update_data():
    return {
        "status": "in progress",
    }
