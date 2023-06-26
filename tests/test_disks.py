from pathlib import Path

from test_macos import DROBO_DISKUTIL_LIST, SONY_SD_DISKUTIL_LIST, DJI_SD_DISKUTIL_LIST

import pytest

from sync_camera_disk import macos
from sync_camera_disk import disks


@pytest.mark.parametrize(
    "input, expected",
    [
        (
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
            DJI_SD_DISKUTIL_LIST,
            [
                disks.DiskMount(
                    path=Path("/Volumes/DJIMini3Pro"),
                    unique_identifier="3a8c3713-c262-3db7-8bec-604865b64393",
                ),
            ],
        ),
        (
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
    ],
    ids=["drobo", "dji", "sony"],
)
def test_mac_disks_to_disk_mounts(
    input: macos.DiskutilList, expected: list[disks.DiskMount]
) -> None:
    assert list(disks.mac_disks_to_disk_mounts(mac_disks=input)) == expected
