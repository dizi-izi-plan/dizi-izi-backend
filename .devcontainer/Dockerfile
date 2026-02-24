FROM python:3.11

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y gdal-bin libgdal-dev postgresql-client gettext
RUN apt-get install nodejs npm -y
RUN npm install -g npm@latest
RUN npm install -g @google/gemini-cli
COPY .devcontainer/settings.json /root/.gemini/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
