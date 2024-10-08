# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.8.1] - 2024-09-19
### Fixed
- Ignore none SHOGUNU files for Atomos Shogun

## [0.8.0] - 2024-09-18
### Fixed
- Fix handling of sub folders when copying files (in particular the ATEM ISO structure). Was flattening the folder structures.

### Added
- Add --no-log-identical-operations to quieten down logs a bit
- Log failures at end of sync

## [0.7.0] - 2024-09-18
### Added
- Add ATEM ISO support

## [0.6.1] - 2024-07-25
### Fixed
- Add missing links to project and code

## [0.6.0] - 2024-07-24
### Fixed
- Switch from black to ruff for formatting

### Added
- Support private/M4root sub-folders in Sony cameras
- Use a match_on config setting to determine which properties to match on. Defaults to uuid, disk size, volume size and volume type.

## [0.5.0] - 2024-02-05
### Added
- Add Atomos support

## [0.4.0] - 2023-08-16
### Added
- Add XDG config location support

## [0.3.0] - 2023-08-15
### Added
- Add GoPro 10 support
- Add Fujifilm X100 support

### Fixed
- Switch to rich for progress bars

## [0.2.0] - 2023-08-11
### Added
- Add tests
- Add a CHANGELOG
- Add support for Insta360 GO 2
- Add support for DJI Osmo Pocket
- Add generate-config command to generate sample configs for connected disks
- Add show-syncs command to show which disks matched up to which configs
- Add Insta360 ONE support

### Fixed
- Only show progress for mounted disks
- Fix CHANGELOG links
- Better handle identifying disks with non-unique unique identifiers via more disk metadata

## [0.1.0] - 2023-05-22
### Added
- Created sync-camera-disk command
- Add support for DJI Mini 3 Pro drone SD card
- Add support for Sony A7 IV memory cards

[Unreleased]: https://github.com/micktwomey/sync-camera-disk/compare/0.8.1...HEAD
[0.8.1]: https://github.com/micktwomey/sync-camera-disk/compare/0.8.0...0.8.1
[0.8.0]: https://github.com/micktwomey/sync-camera-disk/compare/0.7.0...0.8.0
[0.7.0]: https://github.com/micktwomey/sync-camera-disk/compare/0.6.1...0.7.0
[0.6.1]: https://github.com/micktwomey/sync-camera-disk/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/micktwomey/sync-camera-disk/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/micktwomey/sync-camera-disk/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/micktwomey/sync-camera-disk/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/micktwomey/sync-camera-disk/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/micktwomey/sync-camera-disk/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/micktwomey/sync-camera-disk/releases/tag/0.1.0
