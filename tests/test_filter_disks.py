from pathlib import Path

from sync_camera_disk import filter_disks
from sync_camera_disk.config import Config, Destination, Source, SourceType, Sync
from sync_camera_disk.disks import DiskMount


def test_filter_disks_to_syncs() -> None:
    example_sync = Sync(
        destination=Destination(path="/tmp/example"),
        source=Source(
            identifier="example",
            type=SourceType.dji_mini_3_pro,
            disk_size=1234,
            volume_file_system="NTFS",
            volume_name=None,
            volume_size=1230,
        ),
    )
    example_identifier_match_sync = Sync(
        destination=Destination(path="/tmp/unique"),
        source=Source(
            identifier="unique",
            type=SourceType.sony_a7_iv,
            disk_size=5432,
            volume_file_system="NTFS",
            volume_name=None,
            volume_size=5430,
        ),
    )
    example_no_disk_sync = Sync(
        destination=Destination(path="/tmp/no-disk"),
        source=Source(
            identifier="no-disk",
            type=SourceType.dji_osmo_pocket,
            disk_size=1234,
            volume_file_system="NTFS",
            volume_name=None,
            volume_size=1230,
        ),
    )
    example_disk_mount = DiskMount(
        path=Path("/Volumes/Untitled"),
        unique_identifier="example",
        disk_size=1234,
        volume_file_system="NTFS",
        volume_name=None,
        volume_size=1230,
    )
    example_2_disk_mount = DiskMount(
        path=Path("/Volumes/Untitled 1"),
        unique_identifier="example",
        disk_size=5432,
        volume_file_system="NTFS",
        volume_name=None,
        volume_size=5430,
    )
    example_not_synced_disk_mount = DiskMount(
        path=Path("/Volumes/Untitled 2"),
        unique_identifier="not-synced",
        disk_size=5432,
        volume_file_system="NTFS",
        volume_name=None,
        volume_size=5430,
    )
    example_identifier_match_disk_mount = DiskMount(
        path=Path("/Volumes/Untitled 3"),
        unique_identifier="unique",
        disk_size=5432,
        volume_file_system="NTFS",
        volume_name=None,
        volume_size=5430,
    )
    filtered = list(
        filter_disks.filter_disks_to_syncs(
            config=Config(
                syncs=[
                    example_sync,
                    example_identifier_match_sync,
                    example_no_disk_sync,
                ]
            ),
            disks=(  # Emulate an iterable
                d
                for d in [
                    example_disk_mount,
                    example_2_disk_mount,
                    example_not_synced_disk_mount,
                    example_identifier_match_disk_mount,
                ]
            ),
        )
    )
    print(filtered)
    assert filtered == [
        (example_sync, example_disk_mount),
        (example_identifier_match_sync, example_identifier_match_disk_mount),
    ]
