<img alt="Python" src="https://img.shields.io/badge/Python 3.11-1E90FF?stylefor-the-badge&logo=python&logoColor=32CD32"> 
<img alt="Django" src="https://img.shields.io/badge/Django 5.1-1E90FF?stylefor-the-badge&logo=django&logoColor=32CD32">
<img alt="DjangoRESTframework" src="https://img.shields.io/badge/DjangoRESTframework 3.15.2-1E90FF?stylefor-the-badge&logoColor=32CD32">
<img alt="Docker" src="https://img.shields.io/badge/Docker 23.0.3-1E90FF?stylefor-the-badge&logo=docker&logoColor=FFFFFF">
<img alt="Nginx" src="https://img.shields.io/badge/Nginx 1.24-1E90FF?&stylefor-the-badge&logo=nginx&logoColor=32CD32">
<img alt="Postgresql" src="https://img.shields.io/badge/Postgresql 15-1E90FF?&stylefor-the-badge&logo=postgresql&logoColor=FFFFFF">





# Backend сайта "DIZI IZI"

"DiZI IZI" посвящен автоматической планировке помещений.

Пользователю дается возможность внести размеры своего помещения и выбрать мебель, которая там будет стоять. В ответ на полученные данные сайт предоставляет несколько
изображений с уже готовой планировкой. У пользователя есть возможность запросить новую планировку при ее неудовлетворительном качестве.

## Цель проекта

Данный репозиторий - API для сайта "DIZI IZI" совмещенный вместе с алгоритмом обработки данных и вывода координат мебели.

## Технологии
Python 3.11, Django, DRF, Postgres, Docker, Nginx...

## Запуск проекта

Все команды необходимо выполнять в **корневой папке проекта**

1. Установка [Docker](https://www.docker.com/get-started/)
2. Скопировать и настроить переменные окружения в файле .env
    ```bash
     copy .env.example .env
    ```
3. Запуск проекта (доступно по адресу http://localhost:80)
    ```bash
    docker compose up -d
    ```
4. Остановка проекта и удаление контейнеров и базы данных
    ```bash
    docker compose down -v
    ```

Админ панель: http://localhost/admin/ 

Swagger: http://localhost/swagger/

### Дополнительные функции
1. Запуск только базы данных (доступно по адресу localhost:5432)
    ```bash
    docker compose up -d database
    ```
2. Перезапуск проекта
    ```bash
    docker compose restart
    ```
3. Остановка проекта
    ```bash
    docker compose stop
    ```
4. Отправить команду в контейнер
    ```
    docker compose exec -it backend <ваша команда>
    docker compose exec -it database <ваша команда>
    ```
5. Создать суперпользователя:
    ```bash
    docker compose exec -it backend python manage.py createsuperuser
    ```
6. Собрать новый образ (по умолчанию образ скачивается с [DockerHub](https://hub.docker.com/u/diziizi))
    ```bash
    docker compose build
    ```
7. Скачать все образы
    ```bash
    docker compose pull
    ```

### Режим разработки
Docker так же можно использовать во время разработки.
Для этого корневая папка проекта подключается как внешний том контейнера, и все изменения в проекте мгновенно доступны в контейнере.
Перезапуск сервера с новыми файлами происходит автоматически.
`Для разблокировки функционала необходимо в файле docker-compose.yml раскомментировать поле volumes у контейнера backend`
`В файле .env DB_HOST database заменить на localhost.`

### Запуск проекта с выбираемым модулем настроек 
Установите переменную окружения `PATH_TO_SETTINGS_MODULE` в файле `.env`, указав в значении путь к необходимому модулю настроек, например: `'config.settings.develop'`. 
Чтобы вернуться к продакшн настройкам, удалите эту переменную, либо измените её значение на `'config.settings.production'`.

### Установка зависимостей и запуск проекта

   Рекомендуется настроить в проекте папку виртуального окружения
   ```
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

### Загрузка тестовых данных


**Тестовые пользователи**

   ```
   python manage.py loaddata users.json
   ```

### Запуск тестов
   ```
   pip install -r req_dev.txt
   python -m flake8
   python manage.py test
   ```
