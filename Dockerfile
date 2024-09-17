FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN mkdir -p static

RUN pip install poetry && poetry config virtualenvs.create false

RUN poetry install --no-interaction

CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-config /app/log.ini


