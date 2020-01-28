FROM python:3.8

RUN pip install poetry
RUN poetry config settings.virtualenvs.create false

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-dev --no-interaction

COPY . /app

ENV DJANGO_SETTINGS_MODULE=settings_prod
CMD ["./setup_and_run"]
