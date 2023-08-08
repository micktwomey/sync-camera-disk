import tempfile
from pathlib import Path
from typing import Generator

import pytest

from sync_camera_disk import source
from sync_camera_disk.config import SourceType
from sync_camera_disk.disks import DiskMount
from sync_camera_disk.file import File, FileSet


@pytest.fixture
def disk_mount() -> Generator[DiskMount, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        yield DiskMount(path=Path(tmpdir), unique_identifier="abc")


def test_enumerate_source_files_dji_mini_3_pro(disk_mount: DiskMount) -> None:
    media = disk_mount.path / "DCIM" / "100MEDIA"
    media.mkdir(parents=True)
    (media / "DJI_0123.MP4").touch()
    (media / "DJI_0123.SRT").touch()
    file_sets = list(
        source.enumerate_source_files(
            source=disk_mount, source_type=SourceType.dji_mini_3_pro
        )
    )

    # Sort files for comparison
    for fs in file_sets:
        fs.files.sort(key=lambda x: x.path)

    assert file_sets == [
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/100MEDIA/DJI_0123.MP4"),
                File(path=disk_mount.path / "DCIM/100MEDIA/DJI_0123.SRT"),
            ],
            stem="DJI_0123",
            prefix=Path("DCIM/100MEDIA"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        )
    ]


def test_enumerate_source_files_insta360_go_2(disk_mount: DiskMount) -> None:
    media = disk_mount.path / "DCIM" / "Camera01"
    media.mkdir(parents=True)
    (media / "LRV_20210320_172249_01_001.mp4").touch()
    (media / "PRO_LRV_20210320_172314_01_002.mp4").touch()
    (media / "PRO_VID_20210320_172314_00_002.mp4").touch()
    (media / "VID_20210320_172249_00_001.mp4").touch()
    (disk_mount.path / "DCIM" / "fileinfo_list.list").touch()
    file_sets = list(
        source.enumerate_source_files(
            source=disk_mount, source_type=SourceType.insta360_go_2
        )
    )

    # Sort files for comparison
    for fs in file_sets:
        fs.files.sort(key=lambda x: x.path)
    file_sets.sort(key=lambda x: x.files[0].path)

    assert file_sets == [
        FileSet(
            files=[
                File(
                    path=disk_mount.path
                    / "DCIM/Camera01/LRV_20210320_172249_01_001.mp4"
                ),
            ],
            stem="LRV_20210320_172249_01_001",
            prefix=Path("DCIM/Camera01"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(
                    path=disk_mount.path
                    / "DCIM/Camera01/PRO_LRV_20210320_172314_01_002.mp4"
                ),
            ],
            stem="PRO_LRV_20210320_172314_01_002",
            prefix=Path("DCIM/Camera01"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(
                    path=disk_mount.path
                    / "DCIM/Camera01/PRO_VID_20210320_172314_00_002.mp4"
                ),
            ],
            stem="PRO_VID_20210320_172314_00_002",
            prefix=Path("DCIM/Camera01"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(
                    path=disk_mount.path
                    / "DCIM/Camera01/VID_20210320_172249_00_001.mp4"
                ),
            ],
            stem="VID_20210320_172249_00_001",
            prefix=Path("DCIM/Camera01"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
    ]


def test_enumerate_source_files_sony_a7_iv(disk_mount: DiskMount) -> None:
    dcim = disk_mount.path / "DCIM" / "10030620"
    dcim.mkdir(parents=True)
    (dcim / "A7401412.HIF").touch()
    (dcim / "A7401412.ARW").touch()
    m4root = disk_mount.path / "M4ROOT" / "CLIP"
    m4root.mkdir(parents=True)
    (m4root / "C0109M01.XML").touch()
    (m4root / "C0109.MP4").touch()

    file_sets = list(
        source.enumerate_source_files(
            source=disk_mount, source_type=SourceType.sony_a7_iv
        )
    )

    # Sort files for comparison
    for fs in file_sets:
        fs.files.sort(key=lambda x: x.path)
    file_sets.sort(key=lambda fs: fs.stem)

    assert file_sets == [
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/10030620/A7401412.ARW"),
                File(path=disk_mount.path / "DCIM/10030620/A7401412.HIF"),
            ],
            stem="A7401412",
            prefix=Path("DCIM/10030620"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(path=disk_mount.path / "M4ROOT/CLIP/C0109.MP4"),
                File(path=disk_mount.path / "M4ROOT/CLIP/C0109M01.XML"),
            ],
            stem="C0109",
            prefix=Path("M4ROOT/CLIP"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
    ]
