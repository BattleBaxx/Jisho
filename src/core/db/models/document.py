from peewee import AutoField, BigIntegerField, BlobField, BooleanField, CharField, TextField, TimestampField

from src.core.db.models.base import Base


class Document(Base):
    document_id = AutoField()
    file_name = CharField(max_length=255)
    postings = BlobField(default="{}")
    file_location = TextField(null=True)
    file_extension = CharField(null=True)
    user = CharField(null=True)
    size = BigIntegerField(null=True)
    modified = TimestampField(null=True)
    deleted = BooleanField(default=False)
