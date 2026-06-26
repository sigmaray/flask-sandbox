# Flask Cars

Веб-приложение для управления каталогом автомобилей на Flask, SQLAlchemy, Flask-Admin и PostgreSQL.

## Требования

- Python 3.12+
- PostgreSQL (локально или через Docker на порту 5432)
- База данных: `flask-cars`

## Установка

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Создайте базу данных (если ещё не создана):

```bash
PGPASSWORD=postgres psql -h localhost -U postgres -c 'CREATE DATABASE "flask-cars";'
```

Настройки подключения — в файле `.env`:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/flask-cars
SECRET_KEY=dev-secret-change-in-production
FLASK_DEBUG=1
```

## Запуск

```bash
source venv/bin/activate
export FLASK_APP=app.py
flask db upgrade
python app.py
```

Приложение будет доступно по адресу: http://127.0.0.1:5000

Главная страница перенаправляет в админ-панель: http://127.0.0.1:5000/admin

Доступ к админ-панели только для аутентифицированных пользователей. Регистрации на сайте нет — пользователей создают через консоль (см. `flask create-user`).

## Консольные команды

Проект использует [Flask-Migrate](https://flask-migrate.readthedocs.io/) (Alembic) для управления схемой БД.

Перед работой с миграциями задайте переменную окружения:

```bash
export FLASK_APP=app.py
```

### Первичная настройка (один раз)

Если каталог `migrations/` уже есть в репозитории, этот шаг не нужен:

```bash
flask db init
```

### Применить миграции

Создаёт или обновляет таблицы в БД до актуальной версии схемы:

```bash
flask db upgrade
```

### Создать новую миграцию

После изменения моделей в `models.py`:

```bash
flask db migrate -m "Краткое описание изменений"
flask db upgrade
```

Команда `migrate` сгенерирует файл в `migrations/versions/`. Проверьте его перед применением.

### Откатить последнюю миграцию

```bash
flask db downgrade
```

### Текущая версия схемы

```bash
flask db current
flask db history
```

### База уже существует без Alembic

Если таблицы созданы вручную или до подключения миграций, отметьте текущую схему без изменений:

```bash
flask db stamp head
```

## Консольные команды

Для CLI-команд также нужна переменная окружения:

```bash
export FLASK_APP=app.py
```

Список доступных команд:

```bash
flask --help
```

### `flask create-user` — создать пользователя

Интерактивно запрашивает логин, пароль и подтверждение пароля. Созданный пользователь может войти в админ-панель.

```bash
flask create-user
```

### `flask seed-cars` — заполнить таблицу примерами

Добавляет 16 тестовых автомобилей из `seed_data.py`. Если таблица уже содержит записи, команда ничего не делает.

```bash
flask seed-cars
```

Очистить таблицу и заполнить заново:

```bash
flask seed-cars --clear
flask seed-cars --clear -y   # без подтверждения
```

### `flask clear-cars` — очистить таблицу

Удаляет все записи из `cars` и сбрасывает счётчик `id`.

```bash
flask clear-cars
flask clear-cars -y          # без подтверждения
```

### Типичный сценарий для разработки

```bash
flask db upgrade
flask create-user
flask seed-cars
python app.py
```

## Стек

- **Flask** — веб-фреймворк
- **SQLAlchemy + Flask-SQLAlchemy** — ORM и работа с PostgreSQL
- **Flask-Migrate (Alembic)** — миграции схемы БД
- **Flask-Admin** — интерфейс для просмотра, создания, редактирования и удаления записей
- **Flask-Login** — аутентификация для доступа к админ-панели

## Структура проекта

```
app.py           — точка входа, инициализация Flask и Flask-Admin
auth.py          — аутентификация и защита админ-панели
extensions.py    — экземпляр SQLAlchemy
models.py        — модели Car и User
admin_views.py   — настройки админ-панели для автомобилей
cli.py           — консольные команды (create-user, seed-cars, clear-cars)
seed_data.py     — тестовые данные для seed-cars
migrations/      — файлы миграций Alembic
```

## Поля автомобиля

| Поле   | Описание              |
|--------|-----------------------|
| make   | Марка (обязательно)   |
| model  | Модель (обязательно)  |
| year   | Год выпуска           |
| color  | Цвет                  |
| price  | Цена                  |
