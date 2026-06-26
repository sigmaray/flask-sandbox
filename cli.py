import click
from flask.cli import with_appcontext
from sqlalchemy import text

from car_service import clear_cars_table, seed_cars as seed_cars_table
from extensions import db


@click.command("cars-clear")
@click.option("--yes", "-y", is_flag=True, help="Не спрашивать подтверждение.")
@with_appcontext
def clear_cars(yes: bool) -> None:
    """Удалить все записи из таблицы cars."""
    from models import Car

    count = Car.query.count()
    if count == 0:
        click.echo("Таблица cars уже пуста.")
        return

    if not yes and not click.confirm(f"Удалить {count} автомобил(ей) из таблицы cars?"):
        click.echo("Отменено.")
        return

    _, message = clear_cars_table()
    click.echo(message)


@click.command("cars-seed")
@click.option("--clear", "-c", is_flag=True, help="Очистить таблицу перед заполнением.")
@click.option("--yes", "-y", is_flag=True, help="Не спрашивать подтверждение при очистке.")
@with_appcontext
def seed_cars(clear: bool, yes: bool) -> None:
    """Заполнить таблицу cars примерами автомобилей."""
    from models import Car

    existing = Car.query.count()
    if clear and existing:
        if not yes and not click.confirm(
            f"Очистить таблицу ({existing} запис(ей)) и добавить примеры?"
        ):
            click.echo("Отменено.")
            return

    _, message = seed_cars_table(clear=clear)
    click.echo(message)


@click.command("users-clear")
@click.option("--yes", "-y", is_flag=True, help="Не спрашивать подтверждение.")
@with_appcontext
def clear_users(yes: bool) -> None:
    """Удалить все записи из таблицы users."""
    from models import User

    count = User.query.count()
    if count == 0:
        click.echo("Таблица users уже пуста.")
        return

    if not yes and not click.confirm(f"Удалить {count} пользовател(ей) из таблицы users?"):
        click.echo("Отменено.")
        return

    db.session.execute(text("TRUNCATE TABLE users RESTART IDENTITY"))
    db.session.commit()
    click.echo(f"Таблица users очищена. Удалено записей: {count}.")


@click.command("users-create")
@with_appcontext
def create_user() -> None:
    """Создать пользователя для входа в админ-панель."""
    from models import User

    username = click.prompt("Логин").strip()
    if not username:
        click.echo("Логин не может быть пустым.")
        return

    if User.query.filter_by(username=username).first():
        click.echo(f"Пользователь «{username}» уже существует.")
        return

    password = click.prompt("Пароль", hide_input=True)
    password_confirm = click.prompt("Подтверждение пароля", hide_input=True)

    if password != password_confirm:
        click.echo("Пароли не совпадают.")
        return

    if not password:
        click.echo("Пароль не может быть пустым.")
        return

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Пользователь «{username}» создан.")
