import logging

from aiohttp import web

from src.app import init_app
from src.settings import settings


def run():
    app = init_app()
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s: %(module)s: %(levelname)s: %(message)s",
        handlers=[logging.StreamHandler()],
    )
    web.run_app(app, port=settings.WEB_APP_PORT, shutdown_timeout=3)


if __name__ == "__main__":
    run()
