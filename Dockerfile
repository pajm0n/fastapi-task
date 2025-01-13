FROM python:3.11

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache \
  PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry install

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "src.main"]
