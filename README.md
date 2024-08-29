# Distributed app with producer/consumer/aiohttp/rabbitmq/postgresql

<br>
<br>
- well-structured easy to understand and scale-up project structure:

```bash
.
├── README.md
├── docker-compose.yml
├── pyproject.toml
├── .env.example                                                        - env
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
│       ├── config                                                      - config staff
│       │   └── config.py
│       ├── database.py                                                 - global db staff
│       ├── main.py
│       ├── model.py                                                    - global pydantic model
│       ├── rabbit.py
│       ├── settings.py                                                 - global settings staff
│       ├── producer                                                    - producer module
│       │   ├── __init__.py
│       │   └── producer.py
│       └── worker                                                      - worker module
│           ├── __init__.py
│           ├── client.py                                               - web client
│           ├── service.py                                              - services
│           └── worker.py
└── web_app                                                             - web app
    ├── Dockerfile
    ├── alembic                                                         - alembic data
    │   ├── README
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions                                                    - alembic migrations
    ├── alembic.ini
    ├── pytest.ini
    ├── scripts                                                         - scripts
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
    │   ├── database.py                                                 - db staff
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
        └── web
           └── test_client.py
```

- async IO operations
- easy local development
    - Dockerfile optimized for small size and fast builds with a non-root user
    - Docker-compose for easy deployment
    - environment with configured PostgreSQL and RabbitMQ
- SQLAlchemy with slightly configured `alembic`
    - async SQLAlchemy engine
    - migrations set in easy to understand format (`YYYY-MM-DD_HHmm_rev_slug`)
- SQLAlchemy Core query
- RabbitMQ configured with DLX queue
- pydantic model
- aio-pika
- mypy type checked
- pytest, coverage
- linters / format with ruff
- and some other extras, like global custom exceptions, index naming convention, shortcut scripts for alembic, etc...

## Local Development

### Requirements:

docker-compose V2 to support all syntax inside compose .yml

### First Build Only

1. `cp .env.example .env`
2. `docker network create dev`
3. `docker-compose up -d --build`
4. `run db migrations via alembic`

### Migrations

- Create an automatic migration from changes in web_app `src/database.py`

```shell
docker compose exec app_web makemigrations *migration_name*
```

- Run migrations

```shell
docker compose exec app_web migrate
```

- Downgrade migrations

```shell
docker compose exec app_web downgrade -1  # or -2 or base or hash of the migration
```

### Generate data

- Run producer to generate some data into the RabbitMQ queue

```shell
docker compose exec app_consumer generatedata 
```

### Pytest

- Run tests on app_web node

```shell
docker compose exec app_web pytest -v
```

- Run tests with coverage on app_web node

```shell
docker compose exec app_web coverage run -m pytest -v
```

- Run coverage report on app_web node

```shell
docker compose exec app_web coverage report -m
```

### Scale

- Scale up consumer nodes

```shell
docker compose up --scale app_consumer=*2*
```