FROM python:3.12.3-slim

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY --from=requirements . /tmp/requirements

RUN pip install -U pip && \
    pip install --no-cache-dir -r /tmp/requirements/base.txt

RUN pip install --no-cache-dir -r /tmp/requirements/web.txt
RUN pip install --no-cache-dir -r /tmp/requirements/dev.txt

COPY . /src
ENV PATH "$PATH:/src/scripts"

RUN useradd -m -d /src -s /bin/bash app \
    && chown -R app:app /src/* && chmod +x /src/scripts/*

WORKDIR /src
USER app

CMD ["./scripts/start-dev.sh"]