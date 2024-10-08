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


def test_enumerate_source_files_dji_osmo_pocket(disk_mount: DiskMount) -> None:
    # /Volumes/Untitled/DCIM/100MEDIA/DJI_0018.html
    # /Volumes/Untitled/DCIM/100MEDIA/DJI_0019.JPG
    # /Volumes/Untitled/DCIM/100MEDIA/DJI_0020.MOV
    # /Volumes/Untitled/DCIM/100MEDIA/._DJI_0235.MOV
    # /Volumes/Untitled/DCIM/100MEDIA/DJI_0241.MP4
    # /Volumes/Untitled/DCIM/PANORAMA/100_0018/DJI_0001.JPG
    # /Volumes/Untitled/DCIM/PANORAMA/100_0018/DJI_0002.JPG
    media = disk_mount.path / "DCIM" / "100MEDIA"
    media.mkdir(parents=True)
    (media / "DJI_0018.html").touch()
    (media / "DJI_0019.JPG").touch()
    (media / "DJI_0020.MOV").touch()
    (media / "._DJI_0235.MOV").touch()
    (media / "DJI_0241.MP4").touch()

    panorama = disk_mount.path / "DCIM" / "PANORAMA"
    panorama.mkdir(parents=True)
    (panorama / "100_0018").mkdir(parents=True)
    (panorama / "100_0018/DJI_0001.JPG").touch()
    (panorama / "100_0018/DJI_0002.JPG").touch()
    (panorama / "100_0019").mkdir(parents=True)
    (panorama / "100_0019/DJI_0001.JPG").touch()
    (panorama / "100_0019/DJI_0002.JPG").touch()

    file_sets = list(
        source.enumerate_source_files(
            source=disk_mount, source_type=SourceType.dji_osmo_pocket
        )
    )

    # Sort files for comparison
    for fs in file_sets:
        fs.files.sort(key=lambda x: x.path)
    file_sets.sort(key=lambda x: x.files[0].path)

    assert file_sets == [
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/100MEDIA/DJI_0018.html"),
            ],
            stem="DJI_0018",
            prefix=Path("DCIM/100MEDIA"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/100MEDIA/DJI_0019.JPG"),
            ],
            stem="DJI_0019",
            prefix=Path("DCIM/100MEDIA"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/100MEDIA/DJI_0020.MOV"),
            ],
            stem="DJI_0020",
            prefix=Path("DCIM/100MEDIA"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/100MEDIA/DJI_0241.MP4"),
            ],
            stem="DJI_0241",
            prefix=Path("DCIM/100MEDIA"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/PANORAMA/100_0018/DJI_0001.JPG"),
                File(path=disk_mount.path / "DCIM/PANORAMA/100_0018/DJI_0002.JPG"),
            ],
            stem="100_0018",
            prefix=Path("DCIM/PANORAMA/100_0018/"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/PANORAMA/100_0019/DJI_0001.JPG"),
                File(path=disk_mount.path / "DCIM/PANORAMA/100_0019/DJI_0002.JPG"),
            ],
            stem="100_0019",
            prefix=Path("DCIM/PANORAMA/100_0019/"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
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
    m4root_private = disk_mount.path / "private" / "M4ROOT" / "CLIP"
    m4root_private.mkdir(parents=True)
    (m4root_private / "C0110M01.XML").touch()
    (m4root_private / "C0110.MP4").touch()

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
        FileSet(
            files=[
                File(path=disk_mount.path / "private/M4ROOT/CLIP/C0110.MP4"),
                File(path=disk_mount.path / "private/M4ROOT/CLIP/C0110M01.XML"),
            ],
            stem="C0110",
            prefix=Path("private/M4ROOT/CLIP"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
    ]


def test_enumerate_source_files_insta360_one(disk_mount: DiskMount) -> None:
    # /Volumes/Untitled/DCIM/Camera01/IMG_20171217_115531_054.insp
    # /Volumes/Untitled/DCIM/Camera01/._IMG_20171214_180905_018.insp
    # /Volumes/Untitled/DCIM/Camera01/._VID_20171214_180827_017.insv
    # /Volumes/Untitled/DCIM/Camera01/._VID_20171214_181119_020.insv
    # /Volumes/Untitled/DCIM/Camera01/VID_20171222_153701_058.insv
    media = disk_mount.path / "DCIM" / "Camera01"
    media.mkdir(parents=True)
    (media / "IMG_20171217_115531_054.insp").touch()
    (media / "._IMG_20171214_180905_018.insp").touch()
    (media / "._VID_20171214_180827_017.insv").touch()
    (media / "._VID_20171214_181119_020.insv").touch()
    (media / "VID_20171222_153701_058.insv").touch()
    file_sets = list(
        source.enumerate_source_files(
            source=disk_mount, source_type=SourceType.insta360_one
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
                    path=disk_mount.path / "DCIM/Camera01/IMG_20171217_115531_054.insp"
                ),
            ],
            stem="IMG_20171217_115531_054",
            prefix=Path("DCIM/Camera01"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(
                    path=disk_mount.path / "DCIM/Camera01/VID_20171222_153701_058.insv"
                ),
            ],
            stem="VID_20171222_153701_058",
            prefix=Path("DCIM/Camera01"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
    ]


def test_enumerate_source_files_gopro_10(disk_mount: DiskMount) -> None:
    # /Volumes/Untitled/DCIM/100GOPRO/GX010265.MP4
    # /Volumes/Untitled/DCIM/100GOPRO/GL010265.LRV
    # /Volumes/Untitled/DCIM/100GOPRO/GX010265.THM
    # /Volumes/Untitled/DCIM/100GOPRO/GX010266.MP4
    # /Volumes/Untitled/DCIM/100GOPRO/GL010266.LRV
    # /Volumes/Untitled/DCIM/100GOPRO/GX010266.THM
    dcim = disk_mount.path / "DCIM" / "100GOPRO"
    dcim.mkdir(parents=True)
    (dcim / "GX010265.MP4").touch()
    (dcim / "GL010265.LRV").touch()
    (dcim / "GX010265.THM").touch()
    (dcim / "GX010266.MP4").touch()
    (dcim / "GL010266.LRV").touch()
    (dcim / "GX010266.THM").touch()

    file_sets = list(
        source.enumerate_source_files(
            source=disk_mount, source_type=SourceType.gopro_10
        )
    )

    # Sort files for comparison
    for fs in file_sets:
        fs.files.sort(key=lambda x: x.path)
    file_sets.sort(key=lambda fs: fs.stem)

    assert file_sets == [
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/100GOPRO/GL010265.LRV"),
                File(path=disk_mount.path / "DCIM/100GOPRO/GX010265.MP4"),
                File(path=disk_mount.path / "DCIM/100GOPRO/GX010265.THM"),
            ],
            stem="0265",
            prefix=Path("DCIM/100GOPRO"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/100GOPRO/GL010266.LRV"),
                File(path=disk_mount.path / "DCIM/100GOPRO/GX010266.MP4"),
                File(path=disk_mount.path / "DCIM/100GOPRO/GX010266.THM"),
            ],
            stem="0266",
            prefix=Path("DCIM/100GOPRO"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
    ]


def test_enumerate_source_files_fujifilm_x100(disk_mount: DiskMount) -> None:
    # /Volumes/Untitled//DCIM/100_FUJI/DSCF0384.JPG
    # /Volumes/Untitled//DCIM/100_FUJI/DSCF0384.RAF
    dcim = disk_mount.path / "DCIM" / "100_FUJI"
    dcim.mkdir(parents=True)
    (dcim / "DSCF0384.JPG").touch()
    (dcim / "DSCF0384.RAF").touch()
    (dcim / "DSCF0385.JPG").touch()
    (dcim / "DSCF0385.RAF").touch()

    file_sets = list(
        source.enumerate_source_files(
            source=disk_mount, source_type=SourceType.fujifilm_x100
        )
    )

    # Sort files for comparison
    for fs in file_sets:
        fs.files.sort(key=lambda x: x.path)
    file_sets.sort(key=lambda fs: fs.stem)

    assert file_sets == [
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/100_FUJI/DSCF0384.JPG"),
                File(path=disk_mount.path / "DCIM/100_FUJI/DSCF0384.RAF"),
            ],
            stem="DSCF0384",
            prefix=Path("DCIM/100_FUJI"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(path=disk_mount.path / "DCIM/100_FUJI/DSCF0385.JPG"),
                File(path=disk_mount.path / "DCIM/100_FUJI/DSCF0385.RAF"),
            ],
            stem="DSCF0385",
            prefix=Path("DCIM/100_FUJI"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
    ]


def test_enumerate_source_files_atomos_shogun_ultra(disk_mount: DiskMount) -> None:
    # /Volumes/SHOGUNU/SHOGUNU_S001_S001_T001.MOV
    # TODO: other extensions and split files
    ssd = disk_mount.path
    (ssd / "SHOGUNU_S001_S001_T001.MOV").touch()
    (ssd / "SHOGUNU_S001_S001_T002.MOV").touch()
    (ssd / "Frame Grab").mkdir()
    (ssd / "Frame Grab/SHOGUNU_S001_S001_T001.PNG").touch()
    (ssd / "LUT").mkdir()
    (ssd / "LUT/1_SGamut3CineSLog3_To_LC-709.cube").touch()

    file_sets = list(
        source.enumerate_source_files(source=disk_mount, source_type=SourceType.atomos)
    )

    # Sort files for comparison
    for fs in file_sets:
        fs.files.sort(key=lambda x: x.path)
    file_sets.sort(key=lambda fs: fs.stem)

    assert file_sets == [
        FileSet(
            files=[
                File(path=disk_mount.path / "SHOGUNU_S001_S001_T001.MOV"),
            ],
            stem="SHOGUNU_S001_S001_T001",
            prefix=Path(""),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(path=disk_mount.path / "SHOGUNU_S001_S001_T002.MOV"),
            ],
            stem="SHOGUNU_S001_S001_T002",
            prefix=Path(""),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
    ]


def test_enumerate_source_files_atem_extreme_iso_sdi(disk_mount: DiskMount) -> None:
    # /Volumes/ATEM/PyLadies/Video ISO Files/PyLadies CAM 1 01.mp4
    # /Volumes/ATEM/PyLadies/Video ISO Files/._PyLadies CAM 1 01.mp4
    # /Volumes/ATEM/PyLadies/Audio Source Files/PyLadies CAM 1 01.wav
    # /Volumes/ATEM/PyLadies/Audio Source Files/._PyLadies CAM 1 01.wav
    # /Volumes/ATEM/PyLadies/PyLadies 01.mp4
    # /Volumes/ATEM/PyLadies/._PyLadies 01.mp4
    # /Volumes/ATEM/PyLadies/PyLadies.drp
    # /Volumes/ATEM/PyLadies/._PyLadies.drp
    # /Volumes/ATEM/._.

    ssd = disk_mount.path
    (ssd / "PyLadies").mkdir()
    (ssd / "PyLadies/Video ISO Files/").mkdir()
    (ssd / "PyLadies/Video ISO Files/PyLadies CAM 1 01.mp4").touch()
    (ssd / "PyLadies/Video ISO Files/._PyLadies CAM 1 01.mp4").touch()
    (ssd / "PyLadies/Audio Source Files").mkdir()
    (ssd / "PyLadies/Audio Source Files/PyLadies CAM 1 01.wav").touch()
    (ssd / "PyLadies/Audio Source Files/._PyLadies CAM 1 01.wav").touch()
    (ssd / "PyLadies/PyLadies 01.mp4").touch()
    (ssd / "PyLadies/._PyLadies 01.mp4").touch()
    (ssd / "PyLadies/PyLadies.drp").touch()
    (ssd / "PyLadies/._PyLadies.drp").touch()
    (ssd / "._.").touch()
    (ssd / "cat").mkdir()
    (ssd / "cat/Video ISO Files/").mkdir()
    (ssd / "cat/Video ISO Files/cat CAM 1 01.mp4").touch()
    (ssd / "cat/Video ISO Files/cat CAM 2 01.mp4").touch()
    (ssd / "cat/Audio Source Files").mkdir()
    (ssd / "cat/Audio Source Files/cat CAM 1 01.wav").touch()
    (ssd / "cat/Audio Source Files/cat CAM 2 01.wav").touch()
    (ssd / "cat/Video ISO Files/Media Files").mkdir()
    (ssd / "cat/Video ISO Files/Media Files/slide.png").touch()
    (ssd / "cat/cat 01.mp4").touch()
    (ssd / "cat/cat 02.mp4").touch()
    (ssd / "cat/cat.drp").touch()
    (ssd / "cat/cat.drp").touch()

    file_sets = list(
        source.enumerate_source_files(
            source=disk_mount, source_type=SourceType.atem_iso
        )
    )

    # Sort files for comparison
    for fs in file_sets:
        fs.files.sort(key=lambda x: x.path)
    file_sets.sort(key=lambda fs: fs.stem)

    for file_set in file_sets:
        print(f"{file_set.stem=}")
        for file in file_set.files:
            print(f"{file.path.parent.name=} {file.path.name=}")

    assert file_sets == [
        FileSet(
            files=[
                File(
                    path=disk_mount.path
                    / "PyLadies/Audio Source Files/PyLadies CAM 1 01.wav"
                ),
                File(path=disk_mount.path / "PyLadies/PyLadies 01.mp4"),
                File(path=disk_mount.path / "PyLadies/PyLadies.drp"),
                File(
                    path=disk_mount.path
                    / "PyLadies/Video ISO Files/PyLadies CAM 1 01.mp4"
                ),
            ],
            stem="PyLadies",
            prefix=Path("PyLadies"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
        FileSet(
            files=[
                File(path=disk_mount.path / "cat/Audio Source Files/cat CAM 1 01.wav"),
                File(path=disk_mount.path / "cat/Audio Source Files/cat CAM 2 01.wav"),
                File(
                    path=disk_mount.path / "cat/Video ISO Files/Media Files/slide.png"
                ),
                File(path=disk_mount.path / "cat/Video ISO Files/cat CAM 1 01.mp4"),
                File(path=disk_mount.path / "cat/Video ISO Files/cat CAM 2 01.mp4"),
                File(path=disk_mount.path / "cat/cat 01.mp4"),
                File(path=disk_mount.path / "cat/cat 02.mp4"),
                File(path=disk_mount.path / "cat/cat.drp"),
            ],
            stem="cat",
            prefix=Path("cat"),
            volume_identifier="abc",
            volume_path=disk_mount.path,
        ),
    ]
