FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip

# Установка зависимости PostgreSQL
# RUN apt-get update && apt-get install -y libpq-dev gcc
# RUN pip install psycopg2-binary

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000"]