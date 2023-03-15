from peewee import TimestampField

from src.core.db.models.base import Base


class LastIndexed(Base):
    last_indexed = TimestampField(null=True)

    class Meta:
        table_name = "last_indexed"
