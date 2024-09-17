Note App — это простое приложение для создания и управления заметками. Пользователи могут добавлять, редактировать и удалять заметки.


Используемые технологии:
Python, FastAPI, SQLAlchemy, PostgreSQL, aiogram 


Установка и запуск

Клонируйте репозиторий на свой локальный компьютер:
git clone https://github.com/KsuuushkaMerkl/Note-app.git

Проект разворачивается через Docker командой:
$ docker-compose up build

В файл .env нужно добавить параметры:
POSTGRES_HOST=postgres
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432

И API_TOKEN  для работы  Telegram бота.

Документация по проекту будет доступна по адресу http://localhost:8061/docs


