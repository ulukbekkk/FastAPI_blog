FROM python:3.10-slim as builder
WORKDIR /app
## Install poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ENV PATH=$PATH:/etc/poetry/bin

##
ADD ./pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --only main


FROM python:3.10-slim
WORKDIR /app
ENV PATH=/app/.venv/bin:$PATH PYTHONPATH=$PYTHONPATH:/app/src
COPY alembic alembic
COPY alembic.ini .
COPY src src
COPY main.py ./
COPY --from=builder /app/.venv .venv
ENTRYPOINT ["uvicorn", "app:create_app", "--factory", "--loop", "uvloop", "--host", "0.0.0.0", "--port", "8000"]