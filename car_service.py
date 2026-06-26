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
            f"В таблице уже {existing} запис(ей). "
            "Используйте «Очистить и заполнить», чтобы пересоздать данные.",
        )

    if clear and existing:
        db.session.execute(text("TRUNCATE TABLE cars RESTART IDENTITY"))

    for make, model, year, color, price in SAMPLE_CARS:
        db.session.add(Car(make=make, model=model, year=year, color=color, price=price))

    db.session.commit()
    return (
        "success",
        f"Добавлено автомобилей: {len(SAMPLE_CARS)}. Всего в таблице: {Car.query.count()}.",
    )


def clear_cars_table() -> tuple[str, str]:
    """Очистить таблицу cars. Возвращает (category, message)."""
    count = Car.query.count()
    if count == 0:
        return ("info", "Таблица cars уже пуста.")

    db.session.execute(text("TRUNCATE TABLE cars RESTART IDENTITY"))
    db.session.commit()
    return ("success", f"Таблица cars очищена. Удалено записей: {count}.")
