import sys

from src.core.db.connection import DbConnection
from src.core.db.models.document import Document
from src.core.db.models.last_indexed import LastIndexed
from src.core.db.models.term import Term

db = DbConnection.get_connection()

arg = sys.argv[1]

if arg == "up":
    db.create_tables([Term, Document, LastIndexed])

if arg == "down":
    db.drop_tables([Term, Document, LastIndexed])
