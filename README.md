# Distributed app with producer/consumer/aiohttp/rabbitmq/postgresql

- well-structured easy to understand and scale-up project structure

```bash
.
├── README.md
├── docker-compose.yml
├── ruff.toml
├── requirements                                                        - requirements
│   ├── base.txt
│   ├── consumer.txt
│   ├── dev.txt
│   └── web.txt
├── consumer_app                                                        - consumer app
│   ├── Dockerfile
│   ├── scripts                                                         - local scripts
│   │   ├── generatedata
│   │   └── start-dev.sh
│   └── src                                                             - src app module / global settings for modules
│       ├── __init__.py
│       ├── config                                                      
│       │   └── config.py
│       ├── database.py
│       ├── main.py
│       ├── model.py
│       ├── rabbit.py
│       ├── settings.py
│       ├── producer                                                    - producer module
│       │   ├── __init__.py
│       │   └── producer.py
│       └── worker                                                      - worker module
│           ├── __init__.py
│           ├── client.py
│           ├── service.py
│           └── worker.py
└── web_app                                                             - web app
    ├── Dockerfile
    ├── alembic                                                         - alembic data
    │   ├── README
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions
    ├── alembic.ini
    ├── pytest.ini
    ├── scripts
    │   ├── downgrade
    │   ├── makemigrations
    │   ├── migrate
    │   ├── postgres
    │   │   ├── backup
    │   │   └── restore
    │   └── start-dev.sh
    ├── src                                                             - src app module / global settings for modules
    │   ├── __init__.py
    │   ├── app.py
    │   ├── config
    │   │   ├── __init__.py
    │   │   └── config.py
    │   ├── constants.py                                                - global constants
    │   ├── database.py
    │   ├── exception_handlers.py                                       - global exception_handlers
    │   ├── exceptions.py                                               - global exceptions
    │   ├── main.py
    │   ├── model.py                                                    - pydantic model
    │   ├── routes.py
    │   └── settings.py
    │   ├── service
    │   │   ├── __init__.py
    │   │   ├── client.py
    │   │   └── service.py
    └── tests                                                           - tests
        ├── __init__.py
        ├── conftest.py
        └── test_client.py

```

- async IO operations
- easy local development
    - Dockerfile optimized for small size and fast builds with a non-root user
    - Docker-compose for easy deployment
    - environment with configured Postgres and RabbitMQ
- SQLAlchemy with slightly configured `alembic`
    - async SQLAlchemy engine
    - migrations set in easy to understand format (`YYYY-MM-DD_HHmm_rev_slug`)
- SQLAlchemy Core query
- RabbitMQ configured with DLX queue
- pydantic model
- aio-pika 
- pytest
- linters / format with ruff
- and some other extras, like global custom exceptions, index naming convention, shortcut scripts for alembic, etc...

## Local Development

### First Build Only

1. `cp .env.example .env`
2. `docker network create dev`
3. `docker-compose up -d --build`

### Migrations

- Create an automatic migration from changes in web_app `src/database.py`

```shell
docker-compose exec app_web makemigrations *migration_name*
```

- Run migrations

```shell
docker-compose exec app_web migrate
```

- Downgrade migrations

```shell
docker-compose exec app_web downgrade -1  # or -2 or base or hash of the migration
```

- Run producer to generate some data

```shell
docker-compose exec app_consumer generatedata 
```

### Pytest

```shell
docker-compose exec app_web pytest -v
```
