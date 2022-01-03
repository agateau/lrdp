import sqlite3

from datetime import datetime, date, timedelta

from lrdp.db import create_tables, Episode, add_episode
from lrdp.feedgen import select_episodes


def test_select_episodes():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    create_tables(cursor)

    episode_date = datetime.fromisoformat("2022-01-01")
    for idx in range(10):
        episode = Episode(
            id=-1,
            date=episode_date + timedelta(days=idx),
            title=f"Ep {idx}",
            path="/somewhere",
        )
        add_episode(cursor, episode)

    episodes = select_episodes(cursor, datetime.fromisoformat("2022-01-04"), 2)

    assert [x.date.date() for x in episodes] == [
        date.fromisoformat("2022-01-03"),
        date.fromisoformat("2022-01-04"),
    ]
