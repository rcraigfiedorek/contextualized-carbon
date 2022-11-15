FROM python:3.10-slim-bullseye

RUN pip install "poetry==1.2.2"

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN poetry install --no-interaction --no-ansi

COPY . /code/

CMD ["python", "-m", "flask", "run"]

