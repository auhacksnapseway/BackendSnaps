FROM python:3.8

ENV DJANGO_SETTINGS_MODULE=settings_prod

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config settings.virtualenvs.create false
RUN poetry install --no-dev --no-interaction

COPY . /app

CMD ["./setup_and_run"]
