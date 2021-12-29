from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml
from yaml import Loader


@dataclass
class PodcastInfo:
    name: str
    description: str
    website: str
    block_itunes: bool = False

@dataclass
class Config:
    podcast: PodcastInfo
    db_path: Path
    episodes_dir: Path
    episodes_base_url: str
    start_date: datetime
    rss_path: Path


def _parse_date(txt: str) -> datetime:
    date = datetime.fromisoformat(txt)
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)
    return date


def from_yaml(yaml_path: Path) -> Config:
    yaml_path = yaml_path.absolute()
    with yaml_path.open("r") as f:
        dct = yaml.load(f, Loader=Loader)

    yaml_dir = yaml_path.parent

    info = PodcastInfo(**dct["info"])

    cfg = Config(podcast=info,
                 db_path=yaml_dir.joinpath(dct["db_path"]),
                 episodes_dir=yaml_dir.joinpath(dct["episodes_dir"]),
                 episodes_base_url=dct["episodes_base_url"],
                 start_date=_parse_date(dct["start_date"]),
                 rss_path=yaml_dir.joinpath(dct["rss_path"]),
                 )
    if not cfg.episodes_dir.is_dir():
        raise ValueError(f"{cfg.episodes_dir} is not a directory")
    return cfg
