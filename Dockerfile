FROM python:3.12-slim

WORKDIR /app

COPY apps/api/pyproject.toml apps/api/uv.lock apps/api/
COPY apps/api/src apps/api/src
COPY data data
COPY config config

WORKDIR /app/apps/api

RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev

ENV BANKABLE_API_HOST=0.0.0.0
ENV BANKABLE_API_PORT=8080

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "app.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8080"]
