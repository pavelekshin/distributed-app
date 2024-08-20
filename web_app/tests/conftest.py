import pytest
from aiohttp.test_utils import TestClient
from src.app import init_app

# @pytest.fixture(autouse=True, scope="session")
# def run_migrations() -> None:
#     import os
#
#     print("running migrations..")
#     os.system("alembic upgrade head")
#     yield
#     os.system("alembic downgrade base")


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    app = await init_app()
    client: TestClient = await aiohttp_client(app)
    return client
