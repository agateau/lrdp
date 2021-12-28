import datetime

from dataclasses import dataclass

EPISODE_TABLE = "episode"
CREATE_TABLE = f"""
create table {EPISODE_TABLE} (
    id primary key,
    date date,
    title text,
    path text
)
"""

@dataclass
class Episode:
    id: int
    date: datetime.date
    title: str
    path: str
