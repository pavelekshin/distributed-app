import datetime

import pytest
from aiohttp import ClientResponse
from aiohttp.test_utils import TestClient


async def test_healthcheck(client: TestClient):
    resp: ClientResponse = await client.get("/healthcheck")
    assert resp.status == 200
    assert await resp.json() == {"status": "ok"}


async def test_dummy_url(client: TestClient):
    resp: ClientResponse = await client.get("/asd")
    assert resp.status == 404


async def test_validate_code(client: TestClient):
    resp: ClientResponse = await client.post("/123/validate")
    assert resp.status == 404
    assert await resp.json() == {
        "error_code": "Internal Server error",
        "error_message": "Code not found",
        "detail": "Code not found",
    }
