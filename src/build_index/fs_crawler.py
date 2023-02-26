import os
from typing import Generator


class FilesystemCrawler:
    def __init__(self, base_path: str, extensions: list[str]):
        self.base_path = base_path
        self.extensions = set(extensions)

    def get_file_paths(self) -> Generator[str, None, None]:
        for(dir_path, dir_name, file_names) in os.walk(self.base_path):
            for file_name in file_names:
                full_file_name = os.path.join(dir_path, file_name)
                file_extension = os.path.splitext(full_file_name)[-1].lower()
                if file_extension in self.extensions:
                    yield full_file_name
