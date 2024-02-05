import enum
from pathlib import Path

import pydantic


class SourceType(enum.StrEnum):
    unknown = "unknown"
    dji_mini_3_pro = "dji_mini_3_pro"
    dji_osmo_pocket = "dji_osmo_pocket"
    sony_a7_iv = "sony_a7_iv"
    insta360_go_2 = "insta360_go_2"
    insta360_one = "insta360_one"
    gopro_10 = "gopro_10"
    fujifilm_x100 = "fujifilm_x100"
    atomos = "atomos"


class Source(pydantic.BaseModel):
    identifier: str
    type: SourceType
    description: str | None = None
    disk_size: int | None = None
    volume_size: int | None = None
    volume_name: str | None = None
    volume_file_system: str | None = None
    platform: str | None = None


class Destination(pydantic.BaseModel):
    path: Path


class Sync(pydantic.BaseModel):
    source: Source
    destination: Destination


class Config(pydantic.BaseModel):
    syncs: list[Sync]
