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

## Миграции

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

## Стек

- **Flask** — веб-фреймворк
- **SQLAlchemy + Flask-SQLAlchemy** — ORM и работа с PostgreSQL
- **Flask-Migrate (Alembic)** — миграции схемы БД
- **Flask-Admin** — интерфейс для просмотра, создания, редактирования и удаления записей

## Структура проекта

```
app.py           — точка входа, инициализация Flask и Flask-Admin
extensions.py    — экземпляр SQLAlchemy
models.py        — модель Car
admin_views.py   — настройки админ-панели для автомобилей
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
