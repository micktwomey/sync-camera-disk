from typing import Iterable

from .disks import DiskMount
from .file import FileSet, File

from .config import SourceType


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
            all_files_by_prefix = {}
            for p in (source.path / "M4ROOT" / "CLIP").glob("C*"):
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
        case _:
            raise NotImplementedError(source_type)
