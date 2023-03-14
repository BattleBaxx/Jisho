from src.build_index.fs_crawler import FilesystemCrawler
from src.core.config import Config
from src.core.indexing import handle_create

config = Config.get_config("config.json")

crawler = FilesystemCrawler(config["BASE_PATH"], config["EXTENSIONS"])
file_list = list(crawler.get_file_paths())

handle_create(file_list)
