FROM python:3.9-alpine

RUN apk update && apk add --no-cache postgresql-dev

RUN apk add --no-cache curl bash && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    /root/.local/bin/poetry --version

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH=/app

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && poetry install --only=main --no-root --no-interaction --no-ansi

COPY . .

WORKDIR /app/src/bot

ENTRYPOINT ["python", "-u", "main.py"]