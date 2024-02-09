# Dockerize a python app
FROM python:3.11-slim

# Add labels
LABEL author='Dizi-izi-Team'
LABEL maintainer='<https://github.com/dizi-izi-plan>'

# Create app directory
WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN apt-get update && apt-get install -y git
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

#Copy app
COPY . .

ENTRYPOINT ["./docker-entrypoint.sh"]
