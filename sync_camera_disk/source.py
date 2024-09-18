import itertools
from typing import Iterable

import structlog

from .config import SourceType
from .disks import DiskMount
from .file import File, FileSet

LOG: structlog.stdlib.BoundLogger = structlog.get_logger()


def enumerate_source_files(
    source: DiskMount, source_type: SourceType
) -> Iterable[FileSet]:
    all_files_by_prefix: dict[str, FileSet] = {}
    match source_type:
        case SourceType.dji_mini_3_pro:
            # /Volumes/DJIMini3Pro/DCIM/100MEDIA/DJI_0027.{MP4,JPG,DNG,SRT}
            all_files_by_prefix = {}
            for p in (source.path / "DCIM" / "100MEDIA").glob("DJI_*"):
                stem = p.stem
                if stem not in all_files_by_prefix:
                    all_files_by_prefix[stem] = FileSet(
                        files=[],
                        stem=stem,
                        prefix=p.parent.relative_to(source.path),
                        volume_path=source.path,
                        volume_identifier=source.unique_identifier,
                    )
                all_files_by_prefix[stem].files.append(File(path=p))
            yield from all_files_by_prefix.values()
        case SourceType.sony_a7_iv:
            # /Volumes/Untitled 1/DCIM/10030620/A7401412.{ARW,HIF}
            all_files_by_prefix = {}
            for p in (source.path / "DCIM").glob("**/*"):
                if p.exists() and p.is_file() and len(p.suffix) == 4:  # e.g. .ARW
                    stem = p.stem
                    if stem not in all_files_by_prefix:
                        all_files_by_prefix[stem] = FileSet(
                            files=[],
                            stem=stem,
                            prefix=p.parent.relative_to(source.path),
                            volume_path=source.path,
                            volume_identifier=source.unique_identifier,
                        )
                    all_files_by_prefix[stem].files.append(File(path=p))
            yield from all_files_by_prefix.values()

            # /Volumes/Untitled/M4ROOT/CLIP/C0109M01.XML
            # /Volumes/Untitled/M4ROOT/CLIP/C0109.MP4
            # /Volumes/Untitled/private/M4ROOT/CLIP/C0109M01.XML
            # /Volumes/Untitled/private/M4ROOT/CLIP/C0109.MP4
            all_files_by_prefix = {}
            for m4prefix in (source.path, (source.path / "private")):
                for p in (m4prefix / "M4ROOT" / "CLIP").glob("C*"):
                    if p.suffix.lower() == ".xml" and p.stem.lower().endswith("m01"):
                        stem = p.stem[:-3]  # drop M01 portion
                    else:
                        stem = p.stem
                    if stem not in all_files_by_prefix:
                        all_files_by_prefix[stem] = FileSet(
                            files=[],
                            stem=stem,
                            prefix=p.parent.relative_to(source.path),
                            volume_path=source.path,
                            volume_identifier=source.unique_identifier,
                        )
                    all_files_by_prefix[stem].files.append(File(path=p))

            yield from all_files_by_prefix.values()
        case SourceType.insta360_go_2:
            # /Volumes/Insta360GO2/DCIM/Camera01/VID_20210320_172249_00_001.mp4
            # /Volumes/Insta360GO2/DCIM/Camera01/LRV_20210320_172249_01_001.mp4
            # /Volumes/Insta360GO2/DCIM/Camera01/PRO_VID_20210320_172314_00_002.mp4
            # /Volumes/Insta360GO2/DCIM/Camera01/PRO_LRV_20210320_172314_01_002.mp4
            # Probably not needed: /Volumes/Insta360GO2/DCIM/fileinfo_list.list
            all_files_by_prefix = {}
            for p in (source.path / "DCIM" / "Camera01").glob("*"):
                stem = p.stem
                if stem not in all_files_by_prefix:
                    all_files_by_prefix[stem] = FileSet(
                        files=[],
                        stem=stem,
                        prefix=p.parent.relative_to(source.path),
                        volume_path=source.path,
                        volume_identifier=source.unique_identifier,
                    )
                all_files_by_prefix[stem].files.append(File(path=p))
            yield from all_files_by_prefix.values()
        case SourceType.dji_osmo_pocket:
            # /Volumes/Untitled/DCIM/100MEDIA/DJI_0018.html
            # /Volumes/Untitled/DCIM/100MEDIA/DJI_0019.JPG
            # /Volumes/Untitled/DCIM/100MEDIA/DJI_0020.MOV
            # /Volumes/Untitled/DCIM/100MEDIA/._DJI_0235.MOV
            # /Volumes/Untitled/DCIM/100MEDIA/DJI_0241.MP4
            all_files_by_prefix = {}
            for p in (source.path / "DCIM" / "100MEDIA").glob("DJI_*"):
                stem = p.stem
                if stem not in all_files_by_prefix:
                    all_files_by_prefix[stem] = FileSet(
                        files=[],
                        stem=stem,
                        prefix=p.parent.relative_to(source.path),
                        volume_path=source.path,
                        volume_identifier=source.unique_identifier,
                    )
                all_files_by_prefix[stem].files.append(File(path=p))
            yield from all_files_by_prefix.values()

            # /Volumes/Untitled/DCIM/PANORAMA/100_0018
            # /Volumes/Untitled/DCIM/PANORAMA/100_0018/DJI_0001.JPG
            # /Volumes/Untitled/DCIM/PANORAMA/100_0018/DJI_0002.JPG
            all_files_by_prefix = {}
            for p in (source.path / "DCIM" / "PANORAMA").glob("*/DJI_*"):
                stem = p.parent.name
                if stem not in all_files_by_prefix:
                    all_files_by_prefix[stem] = FileSet(
                        files=[],
                        stem=stem,
                        prefix=p.parent.relative_to(source.path),
                        volume_path=source.path,
                        volume_identifier=source.unique_identifier,
                    )
                all_files_by_prefix[stem].files.append(File(path=p))
            yield from all_files_by_prefix.values()
        case SourceType.insta360_one:
            # /Volumes/Untitled/DCIM/Camera01/IMG_20171217_115531_054.insp
            # /Volumes/Untitled/DCIM/Camera01/._IMG_20171214_180905_018.insp
            # /Volumes/Untitled/DCIM/Camera01/._VID_20171214_180827_017.insv
            # /Volumes/Untitled/DCIM/Camera01/._VID_20171214_181119_020.insv
            # /Volumes/Untitled/DCIM/Camera01/VID_20171222_153701_058.insv
            all_files_by_prefix = {}
            for p in (source.path / "DCIM" / "Camera01").glob("*"):
                stem = p.stem
                if stem.startswith("._"):
                    continue
                if stem not in all_files_by_prefix:
                    all_files_by_prefix[stem] = FileSet(
                        files=[],
                        stem=stem,
                        prefix=p.parent.relative_to(source.path),
                        volume_path=source.path,
                        volume_identifier=source.unique_identifier,
                    )
                all_files_by_prefix[stem].files.append(File(path=p))
            yield from all_files_by_prefix.values()
        case SourceType.gopro_10:
            # https://community.gopro.com/s/article/GoPro-Camera-File-Naming-Convention?language=en_US
            # https://community.gopro.com/s/article/What-are-thm-and-lrv-files?language=en_US
            # /Volumes/Untitled/DCIM/100GOPRO/GX010265.MP4
            # /Volumes/Untitled/DCIM/100GOPRO/GL010265.LRV
            # /Volumes/Untitled/DCIM/100GOPRO/GX010265.THM
            all_files_by_prefix = {}
            for p in (source.path / "DCIM" / "100GOPRO").glob("G*"):
                stem = p.stem
                # GFXXYYYY.ext F = Format, XX = chapter/counter/loop, YYYY = file serial
                file_number = stem[-4:]
                if stem.startswith("._"):
                    continue
                if file_number not in all_files_by_prefix:
                    all_files_by_prefix[file_number] = FileSet(
                        files=[],
                        stem=file_number,
                        prefix=p.parent.relative_to(source.path),
                        volume_path=source.path,
                        volume_identifier=source.unique_identifier,
                    )
                all_files_by_prefix[file_number].files.append(File(path=p))
            yield from all_files_by_prefix.values()
        case SourceType.fujifilm_x100:
            # /Volumes/Untitled//DCIM/100_FUJI/DSCF0384.JPG
            # /Volumes/Untitled//DCIM/100_FUJI/DSCF0384.RAF
            all_files_by_prefix = {}
            for p in (source.path / "DCIM" / "100_FUJI").glob("*"):
                stem = p.stem
                if stem.startswith("._"):
                    continue
                if stem not in all_files_by_prefix:
                    all_files_by_prefix[stem] = FileSet(
                        files=[],
                        stem=stem,
                        prefix=p.parent.relative_to(source.path),
                        volume_path=source.path,
                        volume_identifier=source.unique_identifier,
                    )
                all_files_by_prefix[stem].files.append(File(path=p))
            yield from all_files_by_prefix.values()
        case SourceType.atomos:
            # /Volumes/SHOGUNU/SHOGUNU_S001_S001_T001.MOV
            all_files_by_prefix = {}
            for p in (source.path).glob("*"):
                stem = p.stem
                if stem.startswith("."):
                    continue
                if stem.startswith("Frame Grab"):
                    continue
                if stem.startswith(".FF"):
                    continue
                if stem not in all_files_by_prefix:
                    all_files_by_prefix[stem] = FileSet(
                        files=[],
                        stem=stem,
                        prefix=p.parent.relative_to(source.path),
                        volume_path=source.path,
                        volume_identifier=source.unique_identifier,
                    )
                all_files_by_prefix[stem].files.append(File(path=p))
            yield from all_files_by_prefix.values()
        case SourceType.atem_iso:
            # /Volumes/ATEM/PyLadies/Video ISO Files/PyLadies CAM 1 01.mp4
            # /Volumes/ATEM/PyLadies/Video ISO Files/._PyLadies CAM 1 01.mp4
            # /Volumes/ATEM/PyLadies/Audio Source Files/PyLadies CAM 1 01.wav
            # /Volumes/ATEM/PyLadies/Audio Source Files/._PyLadies CAM 1 01.wav
            # /Volumes/ATEM/PyLadies/PyLadies 01.mp4
            # /Volumes/ATEM/PyLadies/._PyLadies 01.mp4
            # /Volumes/ATEM/PyLadies/PyLadies.drp
            # /Volumes/ATEM/PyLadies/._PyLadies.drp
            # /Volumes/ATEM/._.
            all_files_by_prefix = {}
            for p in (source.path).glob("*/*.drp"):
                if p.name.startswith("._"):
                    continue
                stem = p.parent.stem
                if stem not in all_files_by_prefix:
                    all_files_by_prefix[stem] = FileSet(
                        files=[],
                        stem=stem,
                        prefix=p.parent.relative_to(source.path),
                        volume_path=source.path,
                        volume_identifier=source.unique_identifier,
                    )
                    for child in itertools.chain(
                        p.parent.glob("*.mp4"),
                        p.parent.glob("*.drp"),
                        p.parent.glob("Video ISO Files/*.mp4"),
                        p.parent.glob("Video ISO Files/Media Files/*"),
                        p.parent.glob("Audio Source Files/*.wav"),
                    ):
                        if child.name.startswith("._"):
                            continue
                        print((stem, child))
                        all_files_by_prefix[stem].files.append(File(path=child))
            yield from all_files_by_prefix.values()
        case _:
            raise NotImplementedError(source_type)
