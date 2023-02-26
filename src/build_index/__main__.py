from src.build_index.fs_crawler import FilesystemCrawler
from src.build_index.text_processor import TextProcessor
from src.core.config import Config

config = Config.get_config("config.json")

crawler = FilesystemCrawler(config["BASE_PATH"], config["EXTENSIONS"])
file_list = list(crawler.get_file_paths())

for file in file_list:
    content = open(file).read(-1)
    print(TextProcessor.tokenize(content))