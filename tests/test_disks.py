from pathlib import Path
import sys
from typing import Any
from unittest.mock import patch

from test_macos import (
    DROBO_PLIST_OUTPUT,
    DROBO_DISKUTIL_LIST,
    SONY_SD_CARD_PLIST_OUTPUT,
    SONY_SD_DISKUTIL_LIST,
    DJI_SD_CARD_PLIST_OUTPUT,
    DJI_SD_DISKUTIL_LIST,
    DJI_OSMO_POCKET_SD_CARD_PLIST_OUTPUT,
    DJI_OSMO_POCKET_SD_DISKUTIL_LIST,
    INSTA360_GO_2_PLIST_OUTPUT,
    INSTA360_GO_2_DISKUTIL_LIST,
)

import pytest

from sync_camera_disk import macos
from sync_camera_disk import disks


@pytest.mark.parametrize(
    "plist, input, expected",
    [
        (
            DROBO_PLIST_OUTPUT,
            DROBO_DISKUTIL_LIST,
            [
                disks.DiskMount(
                    path=Path("/Volumes/Drobo"),
                    unique_identifier="66edbe2f-3e53-3efa-8475-5a97ca67c53b",
                ),
                disks.DiskMount(
                    path=Path("/Volumes/Drobo2"),
                    unique_identifier="e8c9aa87-2931-3782-a945-ea3eaceeb5b9",
                ),
            ],
        ),
        (
            DJI_SD_CARD_PLIST_OUTPUT,
            DJI_SD_DISKUTIL_LIST,
            [
                disks.DiskMount(
                    path=Path("/Volumes/DJIMini3Pro"),
                    unique_identifier="3a8c3713-c262-3db7-8bec-604865b64393",
                ),
            ],
        ),
        (
            DJI_OSMO_POCKET_SD_CARD_PLIST_OUTPUT,
            DJI_OSMO_POCKET_SD_DISKUTIL_LIST,
            [
                disks.DiskMount(
                    path=Path("/Volumes/Untitled"),
                    unique_identifier="c8bf5026-0077-3f03-aa08-019e0a1dc444",
                ),
            ],
        ),
        (
            SONY_SD_CARD_PLIST_OUTPUT,
            SONY_SD_DISKUTIL_LIST,
            [
                disks.DiskMount(
                    path=Path("/Volumes/DJIMini3Pro"),
                    unique_identifier="3a8c3713-c262-3db7-8bec-604865b64393",
                ),
                disks.DiskMount(
                    path=Path("/Volumes/Untitled"),
                    unique_identifier="ab244049-71f0-37a3-9bd7-c0a5085afe92",
                ),
                disks.DiskMount(
                    path=Path("/Volumes/Untitled 1"),
                    unique_identifier="72f83464-83d9-3c1c-8e25-989d32bf84e5",
                ),
                disks.DiskMount(
                    path=Path("/Volumes/PMHOME"),
                    unique_identifier="63dd74fe-d4c1-37a5-9b36-913b202618bb",
                ),
            ],
        ),
        (
            INSTA360_GO_2_PLIST_OUTPUT,
            INSTA360_GO_2_DISKUTIL_LIST,
            [
                disks.DiskMount(
                    path=Path("/Volumes/Insta360GO2"),
                    unique_identifier="c8bf5026-0077-3f03-aa08-019e0a1dc444",
                ),
            ],
        ),
    ],
    ids=["drobo", "dji", "dji_osmo_pocket", "sony", "insta360_go_2"],
)
def test_mac_disks_to_disk_mounts(
    plist: Any,
    input: macos.DiskutilList,
    expected: list[disks.DiskMount],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert list(disks.mac_disks_to_disk_mounts(mac_disks=input)) == expected

    monkeypatch.setattr(sys, "platform", "darwin")

    with patch(
        "sync_camera_disk.disks.macos.diskutil_list_physical_external_disks"
    ) as diskutil_list_physical_external_disks:
        diskutil_list_physical_external_disks.return_value = plist

        assert list(disks.list_disks()) == expected
