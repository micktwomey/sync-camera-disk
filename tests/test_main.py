import json
import sys
import unittest.mock
from pathlib import Path

import pydantic_yaml
import pytest

from sync_camera_disk import config, main


def test_diskutil_list_physical_external_disks(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with unittest.mock.patch(
        "sync_camera_disk.main.macos.diskutil_list_physical_external_disks"
    ) as mock_diskutil_list_physical_external_disks:
        mock_diskutil_list_physical_external_disks.return_value = {"hello": "world"}
        main.diskutil_list_physical_external_disks()
        assert json.loads(capsys.readouterr().out) == {"hello": "world"}


def test_list_disks(capsys: pytest.CaptureFixture[str]) -> None:
    with unittest.mock.patch(
        "sync_camera_disk.main.sync_camera_disk.disks.list_disks"
    ) as mock_list_disks:
        mock_disks = unittest.mock.Mock()
        mock_disks.json.return_value = json.dumps({"hello": "world"})
        mock_list_disks.return_value = [mock_disks]
        main.list_disks()

        assert json.loads(capsys.readouterr().out) == {"hello": "world"}


@pytest.mark.skipif(sys.platform != "darwin", reason="Only run on Mac")
def test_sync_smoketest(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    with config_path.open("w") as fp:
        fp.write(pydantic_yaml.to_yaml_str(config.Config(syncs=[])))

    main.sync(config_path=config_path, dry_run=True)
    assert "config=Config(syncs=[])" in capsys.readouterr().out
