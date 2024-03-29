# Деплой сервера

## Доступ к серверу

* IP-адрес: 89.111.170.137
* Подключение: используйте SSH для безопасного доступа к серверу:
   ```bash
   ssh root@89.111.170.137
   ```
* Настройка SSH ключей:
  * Для добавления вашего публичного SSH ключа в сервер, скопируйте его в файл `.ssh/authorized_keys` на сервере

#### TODO:
1. [ ] Сменить пользователя root для повышения безопасности

## Скрипт restart.sh

Используйте скрипт `restart.sh` для перезапуска всех контейнеров
   ```bash
   ./restart.sh all
   ```

#### TODO:
1. [ ] Реализация перезапуска отдельных контейнеров


## Docker compose

* **Запуск сервисов:** Используйте `docker-compose up -d` для запуска всех сервисов в фоновом режиме. 
Эта команда также соберет необходимые Docker образы, если они еще не были созданы или обновлены
* **Остановка сервисов:** Вы можете остановить сервисы, используя `docker-compose down`.
Эта команда остановит и удалит все контейнеры, сети и по умолчанию анонимные тома, связанные с вашим docker-compose.yml
* **Обновление сервисов:** Для обновления и перезапуска конкретного сервиса используйте команды:
   ```bash
   docker-compose pull имя_сервиса
   docker-compose up -d --no-deps имя_сервиса
   ```
* Создание внешнего тома для базы данных (необходим для хранения данных вне контейнера)
    ```bash
    docker volume create --name=dizi_postgres_data
    ```

#### TODO:
1. [ ] Вывести логи контейнеров на хост машину


## Настройка Nginx

* Регулярно проверяйте конфигурации на наличие ошибок
   ```bash
   docker compose exec nginx nginx -t
   ```
* Перезагружайте NGINX после внесения изменений
   ```bash
   docker compose exec nginx nginx -s reload
   ```


## Certbot и SSL сертификат

* **Источник:** Воспользуйтесь скриптом и инструкциями из репозитория
[nginx-certbot](https://github.com/wmnnd/nginx-certbot) для настройки SSL сертификатов через Certbot
* **Инициализация сертификата:**
  * Запускайте `init-letsencrypt.sh` только если потеряли сертификат или настраиваете систему в первый раз
  * Внимание: Let's Encrypt имеет ограничение на количество запросов сертификатов - 
  проверьте текущие лимиты (обычно 5 дубликатов сертификата в неделю)
* **Автообновление:** Автоматическое обновление сертификата настроено в `docker-compose.yml`


## Передача секретов

Секреты хранятся в файле `infra/.env`

#### TODO:
1. [ ] Реализовать безопасную передачу и хранение секретов

