# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/micktwomey/sync-camera-disk/compare/0.3.0...HEAD
[0.3.0]: https://github.com/micktwomey/sync-camera-disk/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/micktwomey/sync-camera-disk/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/micktwomey/sync-camera-disk/releases/tag/0.1.0
