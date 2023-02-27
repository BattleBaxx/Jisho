from peewee import AutoField, CharField, TextField, BigIntegerField, TimestampField

from src.core.db.models.base import Base


class Document(Base):
    document_id = AutoField()
    file_name = CharField(max_length=255)
    file_location = TextField(null=True)
    file_extension = CharField(null=True)
    user = CharField(null=True)
    size = BigIntegerField(null=True)
    created = TimestampField(null=True)
    modified = TimestampField(null=True)
