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

Доступ к админ-панели только для аутентифицированных пользователей. Регистрации на сайте нет — пользователей создают через консоль (см. `flask users-create`).

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

### `flask users-create` — создать пользователя

Интерактивно запрашивает логин, пароль и подтверждение пароля. Созданный пользователь может войти в админ-панель.

```bash
flask users-create
```

### `flask cars-seed` — заполнить таблицу примерами

Добавляет 16 тестовых автомобилей из `seed_data.py`. Если таблица уже содержит записи, команда ничего не делает.

```bash
flask cars-seed
```

Очистить таблицу и заполнить заново:

```bash
flask cars-seed --clear
flask cars-seed --clear -y   # без подтверждения
```

### `flask cars-clear` — очистить таблицу

Удаляет все записи из `cars` и сбрасывает счётчик `id`.

```bash
flask cars-clear
flask cars-clear -y          # без подтверждения
```

### Типичный сценарий для разработки

```bash
flask db upgrade
flask users-create
flask cars-seed
python app.py
```

## E2E-тесты (Playwright)

E2E-тесты запускают Flask-приложение в **отдельном окружении**: своя база данных и порт. Dev-сервер на `:5000` и БД `flask-cars` при этом не затрагиваются.

| | Разработка | E2E |
|---|---|---|
| БД | `flask-cars` | `flask-cars-e2e` |
| Порт | `5000` | `5099` |
| Конфиг | `.env` | `.env.e2e` |

### Требования

- Node.js 18+ и npm
- PostgreSQL (та же инстанция, что и для разработки)
- Python-окружение из раздела «Установка» (`venv`, зависимости из `requirements.txt`)

### Установка

```bash
npm install
npx playwright install chromium
```

База `flask-cars-e2e` создаётся автоматически при первом запуске тестов (если установлен `psql`). Вручную:

```bash
PGPASSWORD=postgres psql -h localhost -U postgres -c 'CREATE DATABASE "flask-cars-e2e";'
```

Настройки e2e — в файле `.env.e2e` (уже есть в репозитории):

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/flask-cars-e2e
SECRET_KEY=e2e-secret
FLASK_DEBUG=0
E2E_PORT=5099
```

### Запуск

```bash
npm run test:e2e
```

Другие режимы:

```bash
npm run test:e2e:ui       # интерактивный UI Playwright
npm run test:e2e:headed   # с видимым браузером
```

Playwright сам поднимает Flask через `tests/e2e/start-server.sh`: применяются миграции, очищаются таблицы `cars` и `users`, создаётся пользователь `e2e` / `e2e-pass` для входа в тестах.

### Замечания

- Локально Playwright может переиспользовать уже запущенный сервер на порту `5099`. Если тесты ведут себя странно, остановите процесс на этом порту или запустите с принудительным перезапуском:

  ```bash
  CI=1 npm run test:e2e
  ```

- Отчёты и артефакты Playwright (`playwright-report/`, `test-results/`) добавлены в `.gitignore`.

## Стек

- **Flask** — веб-фреймворк
- **SQLAlchemy + Flask-SQLAlchemy** — ORM и работа с PostgreSQL
- **Flask-Migrate (Alembic)** — миграции схемы БД
- **Flask-Admin** — интерфейс для просмотра, создания, редактирования и удаления записей
- **Flask-Login** — аутентификация для доступа к админ-панели
- **Playwright** — E2E-тесты в браузере

## Структура проекта

```
app.py           — точка входа, инициализация Flask и Flask-Admin
auth.py          — аутентификация и защита админ-панели
extensions.py    — экземпляр SQLAlchemy
models.py        — модели Car и User
admin_views.py   — настройки админ-панели для автомобилей
cli.py           — консольные команды (users-create, cars-seed, cars-clear)
seed_data.py     — тестовые данные для cars-seed
migrations/      — файлы миграций Alembic
.env.e2e         — настройки для E2E-тестов (БД и порт)
scripts/e2e-setup.py — подготовка БД перед E2E-прогоном
tests/e2e/       — Playwright-тесты
playwright.config.ts — конфигурация Playwright
```

## Поля автомобиля

| Поле   | Описание              |
|--------|-----------------------|
| make   | Марка (обязательно)   |
| model  | Модель (обязательно)  |
| year   | Год выпуска           |
| color  | Цвет                  |
| price  | Цена                  |
