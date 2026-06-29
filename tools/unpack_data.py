"""Safely unpack the coordinate archives shipped in ``Data/``."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile


def safe_members(archive: ZipFile, destination: Path):
    destination = destination.resolve()
    for member in archive.infolist():
        target = (destination / member.filename).resolve()
        if not target.is_relative_to(destination):
            raise ValueError(f"Unsafe archive member: {member.filename}")
        yield member


def unpack_archive(archive_path: Path, force: bool = False) -> bool:
    with ZipFile(archive_path) as archive:
        members = list(safe_members(archive, archive_path.parent))
        files = [member for member in members if not member.is_dir()]
        if not force and files and all(
            (archive_path.parent / member.filename).exists() for member in files
        ):
            return False
        archive.extractall(archive_path.parent, members=members)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("Data"))
    parser.add_argument("--force", action="store_true", help="overwrite extracted files")
    args = parser.parse_args()

    archives = sorted(args.data_dir.rglob("*.zip"))
    if not archives:
        raise SystemExit(f"No ZIP archives found below {args.data_dir}")

    extracted = 0
    for archive in archives:
        if unpack_archive(archive, force=args.force):
            extracted += 1
            print(f"Extracted {archive}")
    print(f"Done: {extracted} extracted, {len(archives) - extracted} already present")


if __name__ == "__main__":
    main()
