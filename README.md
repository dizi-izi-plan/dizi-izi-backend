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

4. Сделать миграции в бэке (без явного указания миграции некоторых приложений, миграции не выполняются):
```
docker exec -it backend python manage.py makemigrations
docker exec -it backend python manage.py makemigrations users
docker exec -it backend python manage.py makemigrations info
docker exec -it backend python manage.py migrate
```
6. Создать суперпользователя:
```
docker exec -it backend bash
python manage.py createsuperuser
```
7. Собрать статику:
```
docker exec -it backend bash
python manage.py collectstatic
```

Остановить контейнеры
```
docker-compose stop
```
При запущенных контейнерах для очистки лишних файлов, выполните
```
docker system prune -a
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
