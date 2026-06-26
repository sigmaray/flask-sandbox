from sqlalchemy import text

from extensions import db
from models import Car
from seed_data import SAMPLE_CARS


def seed_cars(*, clear: bool = False) -> tuple[str, str]:
    """Заполнить таблицу cars примерами. Возвращает (category, message)."""
    existing = Car.query.count()
    if existing and not clear:
        return (
            "warning",
            f"The table already has {existing} record(s). "
            "Use Clear and seed to recreate the data.",
        )

    if clear and existing:
        db.session.execute(text("TRUNCATE TABLE cars RESTART IDENTITY"))

    db.session.bulk_insert_mappings(
        Car,
        [
            {"make": make, "model": model, "year": year, "color": color, "price": price}
            for make, model, year, color, price in SAMPLE_CARS
        ],
    )
    db.session.commit()
    return (
        "success",
        f"Added {len(SAMPLE_CARS)} cars. Total in table: {Car.query.count()}.",
    )


def clear_cars_table() -> tuple[str, str]:
    """Очистить таблицу cars. Возвращает (category, message)."""
    count = Car.query.count()
    if count == 0:
        return ("info", "The cars table is already empty.")

    db.session.execute(text("TRUNCATE TABLE cars RESTART IDENTITY"))
    db.session.commit()
    return ("success", f"Cars table cleared. Removed {count} record(s).")
