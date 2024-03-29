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
2. Создание внешнего тома для базы данных (необходим для хранения данных вне контейнера)
    ```bash
    docker volume create --name=diziizi_postgres_data
    ```
3. Запуск проекта (доступно по адресу http://localhost:80)
    ```bash
    docker compose up -d
    ```
4. Остановка проекта с удалением контейнеров
    ```bash
    docker compose down
    ```

Админ панель: http://localhost/admin/ 

Swagger: http://localhost/swagger/

### Дополнительные функции
1. Удаление внешнего тома (стереть базу данных)
    ```bash
    docker volume rm diziizi_postgres_data
    ```
2. Запуск только базы данных (доступно по адресу localhost:5432)
    ```bash
    docker compose up -d database
    ```
3. Перезапуск проекта
    ```bash
    docker compose restart
    ```
4. Остановка проекта
    ```bash
    docker compose stop
    ```
5. Отправить команду в контейнер
    ```
    docker compose exec -it backend <ваша команда>
    docker compose exec -it database <ваша команда>
    ```
6. Создать суперпользователя:
    ```bash
    docker compose exec -it backend python manage.py createsuperuser
    ```
7. Собрать новый образ (по умолчанию образ скачивается с [DockerHub](https://hub.docker.com/u/diziizi))
    ```bash
    docker compose build
    ```
8. Скачать все образы
    ```bash
    docker compose pull
    ```

### Режим разработки
Docker так же можно использовать во время разработки.
Для этого корневая папка проекта подключается как внешний том контейнера, и все изменения в проекте мгновенно доступны в контейнере.
Перезапуск сервера с новыми файлами происходит автоматически.
`Для разблокировки функционала необходимо в файле docker-compose.yml раскомментировать поле volumes у контейнера backend`
`В файле .env.dev DB_HOST заменить на localhost.`


### Установка зависимостей и запуск проекта

   Рекомендуется настроить в проекте папку виртуального окружения
   ```
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
