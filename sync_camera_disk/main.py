import typer

from sync_camera_disk.macos import diskutil_list_physical_external_disks

app = typer.Typer()

# TODO: since every camera names their disk "Untitled" identify using volume UUID


@app.command()
def list_disks():
    disks = diskutil_list_physical_external_disks()
    print(disks.json())
