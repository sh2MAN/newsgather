# NewsGather
### API NewsGather (Сборщик новостей).
API NewsGather - это интерфейс, который позволяет пользователям получать. Последние новости с таких новстных ресурсов как:
 - http://lenta.ru/rss
 - http://www.interfax.ru/rss.asp
 - http://www.kommersant.ru/RSS/news.xml
 - http://www.m24.ru/rss.xml


## Начало работы

Для запуска проекта на локальной машине в целях разработки и тестирования.

### Предварительная подготовка

#### Установка Docker
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop) 
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Установите [Docker Compose](https://docs.docker.com/compose/install/)

### Установка проекта (на примере Linux)

- Создайте папку для проекта NewsGather `mkdir newsgather` и перейдите в нее `cd newsgather`
- Склонируйте этот репозиторий в текущую папку `git clone https://github.com/sh2MAN/newsgather .`.
- Создайте файл `.env` командой `touch .env` и добавьте в него переменные окружения для работы с базой данных:
```sh
POSTGRES_DB=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнер в котором будет развернута БД)
DB_PORT=5432 # порт для подключения к БД
POSTGRES_HOST_AUTH_METHOD=trust
```
- Запустите docker-compose `sudo docker-compose up -d` 

## Тестирование и работа API

Протестировать работу api можно через встроенную документацию http://localhost:8000/docs/
**Подробная документация по API размещена по адресу http://localhost:8000/docs/**

### Алгоритм получение новостей

1. Пользователь отправляет запрос с параметром limit (количество последних новостей, 
является не обязательным) на `/news`.
**Как пример `/news?limit=1`**

## В разработке использованы

* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Loguru](https://loguru.readthedocs.io/en/stable/)
* [Pydantic](https://pydantic-docs.helpmanual.io/)
* [PostgreSQL](https://www.postgresql.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* [Docker](https://www.docker.com/)
* [Uvicorn](https://www.uvicorn.org/)

## Автор

* **Sergei Simonov** - [sh2MAN](https://github.com/sh2MAN)

## License [![BSDv3 license](https://img.shields.io/badge/License-BSDv3-blue.svg)](LICENSE.md)

This project is licensed under the BSD 3 - see the [LICENSE.md](LICENSE.md) file for details