import logging

import httpx

from src.settings import settings

logger = logging.getLogger(__name__)


class Client:
    """
    This is client to communicate with microservice
    """

    BASE_URL: str = f"http://{settings.WEB_APP}:{settings.WEB_APP_PORT}"

    @property
    def client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(base_url=self.BASE_URL, timeout=3.0)

    async def url_validation(self, code: str) -> None:
        async with self.client as client:
            response = await client.post(f"/{code}/validate", data={})
            logger.info(
                f"Response: status={response.status_code} headers={response.headers}"
            )
