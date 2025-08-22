from abc import ABC, abstractmethod
from typing import Any
import csv

from app.settings.initial_settings import PathParams, FakeDBParams
from app.utils import save_updated_db

class AbstractGetOneDAO(ABC):
    @abstractmethod
    def get_one(self, identifier_name: str, identifier_value: Any):
        raise NotImplementedError


class AbstractAddOneDAO(ABC):
    @abstractmethod
    def add_one(self, data: tuple):
        raise NotImplementedError


class AbstractGetPackDAO(ABC):
    @abstractmethod
    def get_pack(self, offset: int, limit: int):
        raise NotImplementedError


class AbstractUpdateOneDAO(ABC):
    @abstractmethod
    def update_one(self, identifier_name: str, identifier_value: Any, data: tuple):
        raise NotImplementedError


class AbstractDeleteOneDAO(ABC):
    @abstractmethod
    def delete_one(self, identifier_name: str, identifier_value: Any):
        raise NotImplementedError


class AddOneItemDAO(AbstractAddOneDAO):
    def add_one(self, data: tuple):
        with open(PathParams.fake_db, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            # writer = csv.DictWriter(file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(data)



class GetOneItemDAO(AbstractGetOneDAO):
    def get_one(self,  identifier_name: str, identifier_value: Any) -> dict[str, Any] | None:
        with open(PathParams.fake_db, encoding='utf-8') as file:
            rows = csv.DictReader(file, delimiter=';', quotechar='"')
            for row in rows:
                if row[identifier_name] == identifier_value:
                    return row


class DeleteItemDAO(AbstractDeleteOneDAO):
    def delete_one(self, identifier_name: str, identifier_value: Any) -> dict[str, Any] | None:
        task_from_db = None

        with open(PathParams.fake_db, "r", encoding="utf-8") as file:
            rows = list(csv.DictReader(file, delimiter=";", quotechar='"'))

        new_rows = []
        for row in rows:
            if row[identifier_name] == str(identifier_value):
                task_from_db = row
                continue
            new_rows.append(row)

        save_updated_db(new_rows)

        return task_from_db


class UpdateOneItemDAO(AbstractUpdateOneDAO):
    def update_one(self, identifier_name: str, identifier_value: Any, data: dict) -> dict[str, Any] | None:
        task_from_db = None

        with open(PathParams.fake_db, "r", encoding="utf-8") as file:
            rows = list(csv.DictReader(file, delimiter=";", quotechar='"'))

        new_rows = []
        for row in rows:
            if row[identifier_name] == str(identifier_value):
                for key, value in data.items():
                    if value is not None and key == "status":
                        row[key] = value.value
                    elif value is not None:
                        row[key] = value
                task_from_db = row
            new_rows.append(row)
        save_updated_db(new_rows)

        return task_from_db


class GetPackItemsDAO(ABC):
    def get_pack(self, offset: int, limit: int) -> list:
        with open(PathParams.fake_db, "r", encoding='utf-8') as file:
            rows = csv.DictReader(file, delimiter=';', quotechar='"')
            return list(rows)[offset:offset + limit]


class TasksDAO(AddOneItemDAO,
               GetOneItemDAO,
               DeleteItemDAO,
               UpdateOneItemDAO,
               GetPackItemsDAO,
               ):
    pass


def get_task_dao() -> TasksDAO:
    return TasksDAO()
