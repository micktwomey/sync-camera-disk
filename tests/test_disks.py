import sys
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
from test_macos import (
    DJI_OSMO_POCKET_SD_CARD_PLIST_OUTPUT,
    DJI_OSMO_POCKET_SD_DISKUTIL_LIST,
    DJI_SD_CARD_PLIST_OUTPUT,
    DJI_SD_DISKUTIL_LIST,
    DROBO_DISKUTIL_LIST,
    DROBO_PLIST_OUTPUT,
    FUJIFILM_X100_DISKUTIL_LIST,
    FUJIFILM_X100_PLIST_OUTPUT,
    GOPRO_10_DISKUTIL_LIST,
    GOPRO_10_PLIST_OUTPUT,
    INSTA360_GO_2_DISKUTIL_LIST,
    INSTA360_GO_2_PLIST_OUTPUT,
    SONY_SD_CARD_PLIST_OUTPUT,
    SONY_SD_DISKUTIL_LIST,
)

from sync_camera_disk import disks, macos


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
                    disk_size=17592186044416,
                    volume_size=17591842070528,
                    volume_name="Drobo",
                    volume_file_system="Apple_HFS",
                ),
                disks.DiskMount(
                    path=Path("/Volumes/Drobo2"),
                    unique_identifier="e8c9aa87-2931-3782-a945-ea3eaceeb5b9",
                    disk_size=17592186044416,
                    volume_size=17591842070528,
                    volume_name="Drobo2",
                    volume_file_system="Apple_HFS",
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
                    disk_size=124675686400,
                    volume_size=124658909184,
                    volume_name="DJIMini3Pro",
                    volume_file_system="Windows_NTFS",
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
                    disk_size=128043712512,
                    volume_size=128026935296,
                    volume_name=None,
                    volume_file_system="Windows_NTFS",
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
                    disk_size=124675686400,
                    volume_size=124658909184,
                    volume_name="DJIMini3Pro",
                    volume_file_system="Windows_NTFS",
                ),
                disks.DiskMount(
                    path=Path("/Volumes/Untitled"),
                    unique_identifier="ab244049-71f0-37a3-9bd7-c0a5085afe92",
                    disk_size=80026361856,
                    volume_size=80009584640,
                    volume_name=None,
                    volume_file_system="Windows_NTFS",
                ),
                disks.DiskMount(
                    path=Path("/Volumes/Untitled 1"),
                    unique_identifier="72f83464-83d9-3c1c-8e25-989d32bf84e5",
                    disk_size=128307953664,
                    volume_size=128291176448,
                    volume_name=None,
                    volume_file_system="Windows_NTFS",
                ),
                disks.DiskMount(
                    path=Path("/Volumes/PMHOME"),
                    unique_identifier="63dd74fe-d4c1-37a5-9b36-913b202618bb",
                    disk_size=67108864,
                    volume_size=67108352,
                    volume_name="PMHOME",
                    volume_file_system="DOS_FAT_32",
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
                    disk_size=30802436608,
                    volume_size=30798242304,
                    volume_name="Insta360GO2",
                    volume_file_system="Windows_NTFS",
                ),
            ],
        ),
        (
            GOPRO_10_PLIST_OUTPUT,
            GOPRO_10_DISKUTIL_LIST,
            [
                disks.DiskMount(
                    path=Path("/Volumes/Untitled"),
                    unique_identifier="d4f5eb21-d08d-3267-8f83-f63cde678b8f",
                    disk_size=511868665856,
                    volume_size=511835111424,
                    volume_name=None,
                    volume_file_system="Windows_NTFS",
                ),
            ],
        ),
        (
            FUJIFILM_X100_PLIST_OUTPUT,
            FUJIFILM_X100_DISKUTIL_LIST,
            [
                disks.DiskMount(
                    path=Path("/Volumes/Untitled"),
                    unique_identifier="Windows_FAT_32-15931539456-15927345152",
                    disk_size=15931539456,
                    volume_size=15927345152,
                    volume_name=None,
                    volume_file_system="Windows_FAT_32",
                ),
            ],
        ),
    ],
    ids=[
        "drobo",
        "dji",
        "dji_osmo_pocket",
        "sony",
        "insta360_go_2",
        "gopro_10",
        "fujifilm_x100",
    ],
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
