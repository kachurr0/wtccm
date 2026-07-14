import os
from pathlib import Path
import shutil
import subprocess
from config import ConfigManager
from datetime import datetime, timedelta

class ArchiveManager:
    def __init__(self, config: ConfigManager):
        self.config = config

    def process_archives(
            self,
            archives: list[Path],
            destination: Path,
            delete_archive: bool = True,
            create_directory: bool = True,
    ):
        for archive in archives:
            self.move_and_extract_archive(
                archive,
                destination,
                delete_archive,
                create_directory,
            )

    def move_and_extract_archive(
            self,
            archive: Path,
            destination: Path,
            delete_archive: bool = True,
            create_directory: bool = True,
    ):
        destination.mkdir(parents=True, exist_ok=True)

        moved_archive = destination / archive.name

        shutil.move(archive, moved_archive)

        if create_directory:
            extract_folder = destination / archive.stem
            extract_folder.mkdir(exist_ok=True)
        else:
            extract_folder = destination

        subprocess.run(
            [
                str(self.config.winrar_path),
                "x",
                str(moved_archive),
                str(extract_folder),
            ],
            check=True,
        )

        if delete_archive:
            moved_archive.unlink()

    def find_recent_archives(self, days: int = 3) -> list[Path]:
        """Возвращает список архивов, изменённых за последние N дней."""

        threshold = datetime.now() - timedelta(days=days)

        return [
            file
            for file in self.config.downloads_path.iterdir()
            if (
                    file.is_file()
                    and file.suffix.lower() in {".rar", ".zip", ".7z"}
                    and datetime.fromtimestamp(file.stat().st_mtime) >= threshold
            )
        ]
