from datetime import datetime

from src.core.config import Config
from src.core.indexing import Indexer
from src.core.last_indexed_dao import get_last_indexed_time, set_last_indexed_time
from src.index.fs_crawler import FilesystemCrawler

config = Config.get_config()

last_indexed_time = get_last_indexed_time()
crawler = FilesystemCrawler(config["BASE_PATH"], config["EXTENSIONS"], last_indexed_time)
file_list = list(crawler.get_file_paths())

indexer = Indexer.get_instance()
indexer.index_files(file_list)
# indexer.mark_deleted(file_list)

current_time = int(datetime.now().timestamp())
set_last_indexed_time(current_time)
