import datetime

import pytest
from aiohttp import ClientResponse
from aiohttp.test_utils import TestClient


async def test_healthcheck(client: TestClient) -> None:
    resp: ClientResponse = await client.get("/healthcheck")
    assert resp.status == 200
    assert await resp.json() == {"status": "ok"}


async def test_nonexistent_endpoint(client: TestClient) -> None:
    resp: ClientResponse = await client.get("/nonexistent_endpoint")
    assert resp.status == 404


async def test_validate_not_found(client: TestClient) -> None:
    resp: ClientResponse = await client.post("/000/validate")
    assert resp.status == 404
    assert await resp.json() == {
        "error_code": "Internal Server error",
        "error_message": "Code not found",
        "detail": "Code not found",
    }


@pytest.mark.parametrize(
    "is_allow_redirect, expected",
    [
        (False, 302),
        (True, 200),
    ],
)
async def test_validate_redirect(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    is_allow_redirect,
    expected,
) -> None:
    from src.routes import client as client_module
    from src.routes import service

    async def fake_request(*args, **kwargs):
        return {
            "id": 10756,
            "message_id": "0",
            "code": "Acos0csqu3E",
            "data": '{"acc_id":"0","unsubscribe":false,"msg_id":"0"}',
            "original_url": "https://pypi.org/",
            "created_at": datetime.datetime.now(),
        }

    async def fake_validation(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_row_by_code", fake_request)
    monkeypatch.setattr(client_module, "check_resource", fake_validation)
    monkeypatch.setattr(service, "insert_message", fake_validation)

    resp: ClientResponse = await client.post(
        "/000/validate", allow_redirects=is_allow_redirect
    )
    assert resp.status == expected
