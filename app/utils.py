import os
import csv
from pathlib import Path

from app.settings.initial_settings import LogParams, PathParams, FakeDBParams


def create_necessary_catalogs():
    logs_catalog = Path().resolve().joinpath(LogParams.logs_catalog)
    if not os.path.exists(logs_catalog):
        os.makedirs(logs_catalog, mode=0o755, exist_ok=True)


def create_fake_db():
    if not os.path.exists(PathParams.fake_db):
        with open(PathParams.fake_db, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=FakeDBParams.field_names,
                delimiter=';',
                quoting=csv.QUOTE_NONNUMERIC,
            )
            writer.writeheader()


def save_updated_db(new_rows: list):
    with open(PathParams.fake_db, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FakeDBParams.field_names,
            delimiter=";",
            quotechar='"',
            quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writeheader()
        writer.writerows(new_rows)
