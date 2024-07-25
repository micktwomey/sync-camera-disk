# Sync Camera Disk

- Code: https://github.com/micktwomey/sync-camera-disk/
- PyPI: https://pypi.org/project/sync-camera-disk/

This is tool for syncing SDs and USB disk mounted cameras to my NAS for later importing into apps.

The goal is to ingest photos and videos onto the NAS and be confident I can delete them off the camera when done.

In addition: multiple sequential runs should be idempotent.

Overall approach:

1. Identify which disks are plugged in
2. Lookup configuration for how to map files
3. Build a list of files to copy (each file should be a set of files to keep related files together)
4. Use mapping to translate files to destination names
5. Lookup files in destination to determine which need to be copied (for existing files use stat to determine if they are the same)
6. (TODO) Build hashes for verification of files

By default treat identically named files which different metadata as an error.
