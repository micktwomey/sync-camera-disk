import enum
from pathlib import Path

import pydantic


class SourceType(enum.StrEnum):
    dji_mini_3_pro = "dji_mini_3_pro"
    dji_osmo_pocket = "dji_osmo_pocket"
    sony_a7_iv = "sony_a7_iv"
    insta360_go_2 = "insta360_go_2"


class Source(pydantic.BaseModel):
    identifier: str
    type: SourceType


class Destination(pydantic.BaseModel):
    path: Path


class Sync(pydantic.BaseModel):
    source: Source
    destination: Destination


class Config(pydantic.BaseModel):
    syncs: list[Sync]
