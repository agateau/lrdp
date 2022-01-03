from dataclasses import dataclass
from datetime import datetime
from sqlite3 import Cursor
from typing import Any, List

EPISODE_TABLE = "episode"
CREATE_TABLE = f"""
create table {EPISODE_TABLE} (
    id integer primary key not null,
    date text not null,
    title text not null,
    path text not null
)
"""


@dataclass
class Episode:
    id: int
    date: datetime
    title: str
    path: str

    @staticmethod
    def from_row(row: List[Any]) -> "Episode":
        return Episode(
            id=row[0], date=datetime.fromisoformat(row[1]), title=row[2], path=row[3]
        )


def create_tables(cursor: Cursor) -> None:
    cursor.execute(CREATE_TABLE)


def add_episode(cursor: Cursor, episode: Episode) -> None:
    cursor.execute(
        f"insert into {EPISODE_TABLE}(date, title, path) values(?, ?, ?)",
        (episode.date, episode.title, episode.path),
    )
