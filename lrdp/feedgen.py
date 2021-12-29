"""
Generates the feed for the podcasts.
"""
import argparse
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from sqlite3 import Cursor
from typing import Iterator
from podgen import Podcast, Episode as PodgenEpisode, Media

from lrdp.config import from_yaml, Config
from lrdp.db import EPISODE_TABLE, Episode


def select_episodes(cursor: Cursor, now: datetime, episode_count) -> Iterator[Episode]:
    now_str = now.strftime("%Y-%m-%d")
    cursor.execute(
        f"select * from {EPISODE_TABLE} where date <= ? order by date limit {episode_count}",
        (now_str,),
    )
    for row in cursor.fetchall():
        yield Episode(*row)


def generate_rss(cfg: Config, now: datetime) -> str:
    podcast = Podcast(
        name=cfg.podcast.name,
        description=cfg.podcast.description,
        website=cfg.podcast.website,
        explicit=False,
        withhold_from_itunes=cfg.podcast.block_itunes,
    )

    conn = sqlite3.connect(cfg.db_path)
    cursor = conn.cursor()

    for episode in select_episodes(cursor, now, episode_count=10):
        path = Path(episode.path)
        rel_path = path.relative_to(cfg.episodes_dir)
        url = cfg.episodes_base_url + str(rel_path)
        media = Media(url, path.stat().st_size)
        episode = PodgenEpisode(title=episode.title, media=media, publication_date=episode.date)
        podcast.episodes.append(episode)

    return podcast.rss_str()


def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__
    )

    parser.add_argument("config", help="Path to the lrdp config file")
    parser.add_argument("--now", help="Override current date")

    args = parser.parse_args()

    cfg = from_yaml(Path(args.config))

    if args.now:
        now = datetime.fromisoformat(args.now)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
    else:
        now = datetime.now(timezone.utc)

    rss_str = generate_rss(cfg, now=now)
    with cfg.rss_path.open("w") as f:
        f.write(rss_str)
