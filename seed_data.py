SAMPLE_SIZE = 2000

_CATALOG = [
    ("Toyota", "Camry", 2023, 2700000),
    ("BMW", "X5", 2021, 5200000),
    ("Mercedes-Benz", "E-Class", 2020, 4800000),
    ("Audi", "A4", 2019, 2900000),
    ("Volkswagen", "Golf", 2018, 1650000),
    ("Hyundai", "Solaris", 2022, 1450000),
    ("Kia", "Rio", 2021, 1380000),
    ("Lada", "Vesta", 2023, 1250000),
    ("Tesla", "Model 3", 2022, 4200000),
    ("Porsche", "911", 2020, 12500000),
    ("Ford", "Focus", 2017, 980000),
    ("Honda", "Civic", 2019, 2100000),
    ("Nissan", "Qashqai", 2021, 2350000),
    ("Skoda", "Octavia", 2020, 1750000),
    ("Mazda", "CX-5", 2022, 3100000),
    ("Renault", "Duster", 2019, 1420000),
    ("Toyota", "RAV4", 2022, 3200000),
    ("BMW", "3 Series", 2020, 3800000),
    ("Mercedes-Benz", "C-Class", 2021, 4100000),
    ("Audi", "Q5", 2022, 4500000),
    ("Volkswagen", "Tiguan", 2021, 2800000),
    ("Hyundai", "Tucson", 2023, 2600000),
    ("Kia", "Sportage", 2022, 2550000),
    ("Lada", "Granta", 2022, 890000),
    ("Tesla", "Model Y", 2023, 5100000),
    ("Ford", "Explorer", 2020, 3400000),
    ("Honda", "Accord", 2021, 2900000),
    ("Nissan", "X-Trail", 2020, 2200000),
    ("Skoda", "Kodiaq", 2021, 3100000),
    ("Mazda", "3", 2023, 1950000),
    ("Renault", "Logan", 2020, 1050000),
    ("Toyota", "Corolla", 2021, 2200000),
    ("BMW", "5 Series", 2019, 4900000),
    ("Mercedes-Benz", "GLC", 2022, 5500000),
    ("Audi", "A6", 2020, 5200000),
    ("Volkswagen", "Polo", 2019, 1350000),
    ("Hyundai", "Creta", 2022, 2100000),
    ("Kia", "K5", 2021, 2400000),
    ("Lada", "Niva", 2021, 1150000),
    ("Porsche", "Cayenne", 2021, 9800000),
]

_COLORS = [
    "Silver",
    "Black",
    "White",
    "Gray",
    "Red",
    "Blue",
    "Green",
    "Orange",
    "Beige",
    "Yellow",
    "Brown",
    "Purple",
]


def _build_sample_cars() -> list[tuple[str, str, int, str, int]]:
    cars: list[tuple[str, str, int, str, int]] = []
    catalog_len = len(_CATALOG)
    for i in range(SAMPLE_SIZE):
        make, model, base_year, base_price = _CATALOG[i % catalog_len]
        year = base_year - (i // catalog_len) % 10
        color = _COLORS[i % len(_COLORS)]
        price = base_price + (i % 25) * 40_000 - (i % 13) * 25_000
        price = max(500_000, price)
        cars.append((make, model, year, color, price))
    return cars


SAMPLE_CARS = _build_sample_cars()
