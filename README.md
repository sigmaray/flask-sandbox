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
python app.py
```

Приложение будет доступно по адресу: http://127.0.0.1:5000

Главная страница перенаправляет в админ-панель: http://127.0.0.1:5000/admin

Таблица `cars` создаётся автоматически при первом запуске (если ещё не существует).

## Стек

- **Flask** — веб-фреймворк
- **SQLAlchemy + Flask-SQLAlchemy** — ORM и работа с PostgreSQL
- **Flask-Admin** — интерфейс для просмотра, создания, редактирования и удаления записей

## Структура проекта

```
app.py           — точка входа, инициализация Flask и Flask-Admin
extensions.py    — экземпляр SQLAlchemy
models.py        — модель Car
admin_views.py   — настройки админ-панели для автомобилей
```

## Поля автомобиля

| Поле   | Описание              |
|--------|-----------------------|
| make   | Марка (обязательно)   |
| model  | Модель (обязательно)  |
| year   | Год выпуска           |
| color  | Цвет                  |
| price  | Цена                  |
