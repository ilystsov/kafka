FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY src ./src
COPY tests ./tests
RUN poetry config virtualenvs.create false \
    && poetry install

CMD ["python", "-m", "src.homework.consumer"]
