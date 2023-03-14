from src.core.db.models.base import Base
from peewee import TextField, AutoField, BlobField, IntegerField


class Term(Base):
    term_id = AutoField()
    term = TextField(unique=True)
    doc_list = BlobField(default="[]")
    df = IntegerField(null=True)

    def __str__(self):
        return f"Term: {self.term}, ID: {self.term_id}"
