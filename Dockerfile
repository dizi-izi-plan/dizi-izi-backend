# Dockerize a python app
FROM python:3.11.8-slim

# Add labels
LABEL author='Dizi-izi-Team'
LABEL maintainer='<https://github.com/dizi-izi-plan>'

# Create app directory
WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN apt-get update && \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir && \
    apt-get install -y gdal-bin libgdal-dev postgresql-client gettext && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#Copy app
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Compilation of translation binary file
RUN python manage.py compilemessages

RUN chmod +x docker-entrypoint.sh

# Switch from 'root' to 'doc_user' for more safety
RUN adduser --disabled-password --gecos '' doc_user
USER doc_user

# Run app
ENTRYPOINT ["./docker-entrypoint.sh"]
