from dataclasses import dataclass, field

"""

cameras:
  mycamera:
    - plugin: gphoto2
    - plugin: filter_filename_globs
      params:
        action: include
        case_insensitive: true
        globs:
        - "*.JPG"
    - plugin: destination_folder
      params:
        path: /Volumes/Cameras/ATEM SDI Extreme ISO
        date_structure: true

"""


@dataclass
class Plugin:
    plugin: str
    params: dict[str, str | list[str] | bool] = field(default_factory=dict)


@dataclass
class CameraConfig:
    source: Plugin
    filters: list[Plugin]
    destination: Plugin


@dataclass
class Config:
    cameras: list[CameraConfig]


def main() -> None:
    Config(
        cameras=[
            CameraConfig(
                source=Plugin(plugin="gphoto2"),
                filters=[
                    Plugin(
                        plugin="filter_filename_globs",
                        params={
                            "action": "include",
                            "case_insensitive": True,
                            "globs": ["*.jpg"],
                        },
                    ),
                ],
                destination=Plugin(
                    plugin="destination_folder",
                    params={
                        "path": "/Volumes/Cameras/ATEM SDI Extreme ISO",
                        "date_structure": True,
                    },
                ),
            )
        ]
    )


if __name__ == "__main__":
    main()
