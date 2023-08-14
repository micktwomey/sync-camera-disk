import datetime
import shutil
from pathlib import Path

from sync_camera_disk import destination
from sync_camera_disk.file import File, FileSet
from sync_camera_disk.operation import Operation, OperationType


def test_is_file_identical(tmp_path: Path) -> None:
    foo = tmp_path / "foo" / "file.mp4"
    bar = tmp_path / "bar" / "file.mp4"
    foo.parent.mkdir()
    foo.touch()
    with foo.open("w") as fp:
        fp.write("ham")
    bar.parent.mkdir()
    bar.touch()
    assert destination.is_file_identical(foo, foo)
    assert destination.is_file_identical(bar, bar)
    assert not destination.is_file_identical(foo, bar)

    shutil.copy2(foo, bar)
    assert destination.is_file_identical(foo, foo)
    assert destination.is_file_identical(bar, bar)
    assert destination.is_file_identical(foo, bar)


def test_dated_folder_destination(tmp_path: Path) -> None:
    dest = destination.DatedFolderDestination(prefix=tmp_path / "destination")

    file1 = File(path=tmp_path / "source" / "abc.mp4")
    file1.path.parent.mkdir(parents=True, exist_ok=True)
    file1.path.touch()
    file2 = File(path=tmp_path / "source" / "abc.srt")
    file2.path.parent.mkdir(parents=True, exist_ok=True)
    file2.path.touch()
    file3 = File(path=tmp_path / "source" / "abc.txt")
    file3.path.parent.mkdir(parents=True, exist_ok=True)
    with file3.path.open("w") as fp:
        fp.write("hello")
    file4 = File(path=tmp_path / "source" / "abc.text")
    file4.path.parent.mkdir(parents=True, exist_ok=True)
    with file4.path.open("w") as fp:
        fp.write("ham")

    today = datetime.date.today()
    date = today.isoformat()

    p = tmp_path / "destination" / date / "prefix" / "abc.txt"
    p.parent.mkdir(exist_ok=True, parents=True)
    p.touch()

    assert not destination.is_file_identical(file3.path, p)

    p = tmp_path / "destination" / date / "prefix" / "abc.text"
    p.parent.mkdir(exist_ok=True, parents=True)
    with p.open("w") as fp:
        fp.write("ham")

    assert destination.is_file_identical(file4.path, p)

    operations = list(
        dest.generate_operations(
            file_set=FileSet(
                files=[file1, file2, file3, file4],
                stem="abc",
                prefix=Path("prefix"),
                volume_path=tmp_path / "source",
                volume_identifier="abc",
            )
        )
    )

    assert operations == [
        Operation(
            operation=OperationType.copy,
            source=file1.path,
            destination=tmp_path / "destination" / date / "prefix" / "abc.mp4",
        ),
        Operation(
            operation=OperationType.copy,
            source=file2.path,
            destination=tmp_path / "destination" / date / "prefix" / "abc.srt",
        ),
        Operation(
            operation=OperationType.unknown,
            source=file3.path,
            destination=tmp_path / "destination" / date / "prefix" / "abc.txt",
        ),
        Operation(
            operation=OperationType.identical,
            source=file4.path,
            destination=tmp_path / "destination" / date / "prefix" / "abc.text",
        ),
    ]
