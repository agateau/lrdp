"""
(Re-)creates a database for a directory of podcasts.
"""
import argparse
import datetime
import sqlite3
from pathlib import Path
from sqlite3 import Cursor

from lrdp.config import Config, from_yaml
from lrdp.db import EPISODE_TABLE, CREATE_TABLE


def compute_next_date(date: datetime.date) -> datetime.date:
    while True:
        date += datetime.timedelta(days=1)
        if date.weekday() < 5:
            return date


def get_title(mp3_path: Path) -> str:
    return mp3_path.stem.replace("-", " ")


def table_exists(cursor: Cursor, name: str) -> bool:
    cursor.execute("select * from sqlite_master where type='table' and name=?", (name,))
    return cursor.fetchone() is not None


class App:
    def __init__(self, cfg: Config):
        self.conn = sqlite3.connect(cfg.db_path)
        self.cursor = self.conn.cursor()
        self.next_date = compute_next_date(cfg.start_date - datetime.timedelta(days=1))

    def create_table(self) -> None:
        if table_exists(self.cursor, EPISODE_TABLE):
            self.cursor.execute(f"delete from {EPISODE_TABLE}")
        else:
            self.cursor.execute(CREATE_TABLE)

    def add_episode(self, mp3_path: Path) -> None:
        title = get_title(mp3_path)
        self.cursor.execute(f"insert into {EPISODE_TABLE}(date, title, path) values(?, ?, ?)",
                            (self.next_date, title, str(mp3_path)))
        self.next_date = compute_next_date(self.next_date)

    def finish(self):
        self.conn.commit()


def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)

    parser.add_argument("config", help="Path to the lrdp config file")

    args = parser.parse_args()

    cfg = from_yaml(Path(args.config))

    app = App(cfg)
    app.create_table()

    for mp3 in sorted(cfg.episodes_dir.rglob("*.mp3")):
        app.add_episode(mp3)
    app.finish()
