import datetime
from pathlib import Path
from typing import Any, Iterable

import gphoto2 as gp
from rich import print


def list_files(
    camera: Any, folder: Path
) -> Iterable[tuple[str, str, int, int, int, datetime.datetime]]:
    for filename in camera.folder_list_files(str(folder)).keys():
        info = camera.file_get_info(str(folder), filename)
        yield (
            str(folder),
            filename,
            info.file.width,
            info.file.height,
            info.file.size,
            datetime.datetime.fromtimestamp(info.file.mtime),
        )
    for child in camera.folder_list_folders(str(folder)).keys():
        yield from list_files(camera, folder / child)


camera = gp.check_result(gp.gp_camera_new())
gp.check_result(gp.gp_camera_init(camera))
text = gp.check_result(gp.gp_camera_get_summary(camera))
print("Summary")
print("=======")
print(text.text)

for info in list_files(camera, Path("/")):
    print(info)

gp.check_result(gp.gp_camera_exit(camera))
