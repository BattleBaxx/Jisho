from peewee import Model

from src.core.db.connection import DbConnection

db = DbConnection.get_connection()


class Base(Model):
    class Meta:
        database = db
