import click
from flask.cli import with_appcontext

from car_service import clear_cars_table, seed_cars as seed_cars_table


@click.command("clear-cars")
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


@click.command("seed-cars")
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
