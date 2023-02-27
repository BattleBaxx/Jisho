from peewee import SqliteDatabase


class DbConnection:
    connection = None

    @staticmethod
    def get_connection():
        if DbConnection.connection is None:
            DbConnection.connection = SqliteDatabase("index.db")
            DbConnection.connection.connect()

        return DbConnection.connection
