import click
from flask.cli import with_appcontext
from sqlalchemy import text

from extensions import db
from models import Car
from seed_data import SAMPLE_CARS


@click.command("clear-cars")
@click.option("--yes", "-y", is_flag=True, help="Не спрашивать подтверждение.")
@with_appcontext
def clear_cars(yes: bool) -> None:
    """Удалить все записи из таблицы cars."""
    count = Car.query.count()
    if count == 0:
        click.echo("Таблица cars уже пуста.")
        return

    if not yes and not click.confirm(f"Удалить {count} автомобил(ей) из таблицы cars?"):
        click.echo("Отменено.")
        return

    db.session.execute(text("TRUNCATE TABLE cars RESTART IDENTITY"))
    db.session.commit()
    click.echo(f"Таблица cars очищена. Удалено записей: {count}.")


@click.command("seed-cars")
@click.option("--clear", "-c", is_flag=True, help="Очистить таблицу перед заполнением.")
@click.option("--yes", "-y", is_flag=True, help="Не спрашивать подтверждение при очистке.")
@with_appcontext
def seed_cars(clear: bool, yes: bool) -> None:
    """Заполнить таблицу cars примерами автомобилей."""
    existing = Car.query.count()
    if existing and not clear:
        click.echo(
            f"В таблице уже {existing} запис(ей). "
            "Используйте --clear, чтобы очистить и заполнить заново."
        )
        return

    if clear:
        if existing:
            if not yes and not click.confirm(
                f"Очистить таблицу ({existing} запис(ей)) и добавить примеры?"
            ):
                click.echo("Отменено.")
                return
            db.session.execute(text("TRUNCATE TABLE cars RESTART IDENTITY"))

    for make, model, year, color, price in SAMPLE_CARS:
        db.session.add(Car(make=make, model=model, year=year, color=color, price=price))

    db.session.commit()
    click.echo(f"Добавлено автомобилей: {len(SAMPLE_CARS)}. Всего в таблице: {Car.query.count()}.")
