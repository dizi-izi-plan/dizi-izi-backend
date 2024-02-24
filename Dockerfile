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
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch from 'root' to 'doc_user' for more safety
RUN adduser --disabled-password --gecos '' doc_user
USER doc_user

#Copy app
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run app
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
