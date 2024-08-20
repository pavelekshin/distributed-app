import logging

from dynaconf import Dynaconf

from src.config.config import PostgreSQL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(module)s: %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()],
)

settings = Dynaconf(
    envvar_prefix=False,
    load_dotenv=True,
)

db_settings = PostgreSQL(url=settings.DATABASE_URL, echo=True)
