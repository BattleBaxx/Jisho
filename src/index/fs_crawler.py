import os
from typing import Iterator

from src.core.util import get_file_metadata


class FilesystemCrawler:
    def __init__(self, base_path: str, extensions: list[str]):
        self.base_path = base_path
        self.extensions = set(extensions)

    def get_file_paths(self, last_indexed_time: int) -> Iterator[str]:
        for dir_path, dir_name, file_names in os.walk(self.base_path):
            for file_name in file_names:
                full_file_name = os.path.join(dir_path, file_name)
                file_extension = os.path.splitext(full_file_name)[-1].lower()
                file_metadata = get_file_metadata(full_file_name)
                if file_extension in self.extensions and file_metadata.modified > last_indexed_time:
                    yield full_file_name
