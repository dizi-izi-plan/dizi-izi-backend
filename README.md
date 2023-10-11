# Backend сайта "DIZI IZI"

"DiZI IZI" посвящен автоматической планировке помещений.

Пользователю дается возможность внести размеры своего помещения и выбрать мебель, которая там будет стоять. В ответ на полученные данные сайт предоставляет несколько
изображений с уже готовой планировкой. У пользователя есть возможность запросить новую планировку при ее неудовлетворительном качестве.

## Цель проекта

Данный репозиторий - API для сайта "DIZI IZI" совмещенный вместе с алгоритмом обработки данных и вывода координат мебели.

## Технологии:
Python 3.11, Django, DRF, Postgres, Docker, Nginx...

### Запустить проект локально
1. Скачать Docker Desktop
2. Создать в директории проекта файл '.env' и заполнить:
```python
DJANGO_KEY=''
DEBUG_KEY=True
ALLOWED_HOSTS=localhost,*
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```
3. Перейти в директорию проекта в папку `\infra` и выполнить команды:
```
docker-compose up -d --build
```
4. Создать базу данных в контейнере `postgres`. В процессе доработки создание базы из переменных окружения.
```
docker exec -it <id_container> bash
```
```postgresql
psql -U postgres
CREATE DATABASE <data_base_name>;
```
5. Сделать миграции в бэке (без явного указания миграции некоторых приложений, миграции не выполняются):
```
docker exec -it <id_container> python manage.py makemigrations
docker exec -it <id_container> python manage.py makemigrations users
docker exec -it <id_container> python manage.py makemigrations info
docker exec -it <id_container> python manage.py migrate
```
6. Создать суперпользователя:
```
docker exec -it <id_container> bash
python manage.py createsuperuser
```
7. Собрать статику:
```
docker exec <id_container> python manage.py collectstatic
```
Можно запустить команды по имени контейнера.
```
docker exec backend python manage.py collectstatic
```

Бэкенд будет доступен по адресу `http://localhost`
Админка будет доступена по адресу `http://localhost/admin`
### Install Dependencies and Run App

```
make install
```

```
make run-backend
```
