from peewee import SqliteDatabase

from src.core.config import Config

config = Config.get_config()


class DbConnection:
    connection = None

    @staticmethod
    def get_connection():
        if DbConnection.connection is None:
            DbConnection.connection = SqliteDatabase(config["DB_PATH"])
            DbConnection.connection.connect()

        return DbConnection.connection
