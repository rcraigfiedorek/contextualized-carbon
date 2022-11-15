FROM python:3.10-slim-bullseye

ARG POETRY_VERSION

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN poetry install --no-interaction --no-ansi

COPY . /code/

CMD ["python", "-m", "flask", "run"]

