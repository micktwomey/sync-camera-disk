import sys
from typing import Any

import pytest

from sync_camera_disk.macos import (
    DiskutilList,
    diskutil_list_physical_external_disks,
    parse_diskutil_output,
)
from sync_camera_disk.testing.examples import (
    ATEM_EXTREME_ISO_SDI_DISKUTIL_LIST,
    ATEM_EXTREME_ISO_SDI_PLIST_OUTPUT,
    ATOMOS_SHOGUN_ULTRA_DISKUTIL_LIST,
    ATOMOS_SHOGUN_ULTRA_PLIST_OUTPUT,
    DJI_OSMO_POCKET_SD_CARD_PLIST_OUTPUT,
    DJI_OSMO_POCKET_SD_DISKUTIL_LIST,
    DJI_SD_CARD_PLIST_OUTPUT,
    DJI_SD_DISKUTIL_LIST,
    DROBO_DISKUTIL_LIST,
    DROBO_PLIST_OUTPUT,
    FUJIFILM_X100_DISKUTIL_LIST,
    FUJIFILM_X100_PLIST_OUTPUT,
    FUJIFILM_XE5_DISKUTIL_LIST,
    FUJIFILM_XE5_PLIST_OUTPUT,
    GOPRO_10_DISKUTIL_LIST,
    GOPRO_10_PLIST_OUTPUT,
    INSTA360_GO_2_DISKUTIL_LIST,
    INSTA360_GO_2_PLIST_OUTPUT,
    INSTA360_ONE_DISKUTIL_LIST,
    INSTA360_ONE_PLIST_OUTPUT,
    SONY_SD_CARD_PLIST_OUTPUT,
    SONY_SD_DISKUTIL_LIST,
)


@pytest.mark.parametrize(
    "plist_output,expected",
    [
        (DROBO_PLIST_OUTPUT, DROBO_DISKUTIL_LIST),
        (DJI_OSMO_POCKET_SD_CARD_PLIST_OUTPUT, DJI_OSMO_POCKET_SD_DISKUTIL_LIST),
        (DJI_SD_CARD_PLIST_OUTPUT, DJI_SD_DISKUTIL_LIST),
        (SONY_SD_CARD_PLIST_OUTPUT, SONY_SD_DISKUTIL_LIST),
        (INSTA360_GO_2_PLIST_OUTPUT, INSTA360_GO_2_DISKUTIL_LIST),
        (INSTA360_ONE_PLIST_OUTPUT, INSTA360_ONE_DISKUTIL_LIST),
        (GOPRO_10_PLIST_OUTPUT, GOPRO_10_DISKUTIL_LIST),
        (FUJIFILM_X100_PLIST_OUTPUT, FUJIFILM_X100_DISKUTIL_LIST),
        (ATOMOS_SHOGUN_ULTRA_PLIST_OUTPUT, ATOMOS_SHOGUN_ULTRA_DISKUTIL_LIST),
        (ATEM_EXTREME_ISO_SDI_PLIST_OUTPUT, ATEM_EXTREME_ISO_SDI_DISKUTIL_LIST),
        (FUJIFILM_XE5_PLIST_OUTPUT, FUJIFILM_XE5_DISKUTIL_LIST),
    ],
    ids=[
        "drobo",
        "dji_osmo_pocket_sd_card",
        "dji_sd_card",
        "sony_a7_iv",
        "insta360_go_2",
        "insta360_one",
        "gopro_10",
        "fujifilm_x100",
        "atomos",
        "atem",
        "fujifilm_xe5",
    ],
)
def test_parse_plist_output(plist_output: Any, expected: DiskutilList) -> None:
    # Do the dict version first for nicer diffs
    # TODO: find a pydantic mypy plugin for nice diffs
    assert parse_diskutil_output(plist_output).dict() == expected.dict()
    assert parse_diskutil_output(plist_output) == expected


@pytest.mark.skipif(sys.platform != "darwin", reason="Only run on Mac")
def test_diskutil_list_physical_external_disks_runs() -> None:
    assert isinstance(diskutil_list_physical_external_disks(), dict)
