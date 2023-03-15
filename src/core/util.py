from collections import namedtuple
from pathlib import Path

FileMetadata = namedtuple("FileMetadata", "user size modified")


def get_file_metadata(file_path: str):
    path = Path(file_path)
    path_stat = path.stat()
    return FileMetadata(path.owner(), path_stat.st_size, int(path_stat.st_mtime))
