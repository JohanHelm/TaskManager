from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppParams:
    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8155
    reload: bool = True
    workers: int = 1


@dataclass(frozen=True)
class PathParams:
    workdir: Path = Path().resolve()
    fake_db: Path = workdir.joinpath("fake_db/tasks.csv")


@dataclass(frozen=True)
class FakeDBParams:
    field_names: tuple[str] = ("id", "name", "description", "status")


@dataclass(frozen=True)
class LogParams:
    loglevel: int = 10
    log_max_size: int = 10
    log_file_mode: str = "w"
    backup_count: int = 10
    logs_catalog: Path = Path().resolve().joinpath("logs")
    logs_encoding: str = "utf-8"
