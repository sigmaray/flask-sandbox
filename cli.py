import click
from flask.cli import with_appcontext
from sqlalchemy import text

from extensions import db
from models import Car


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
