from src.core.db.models.last_indexed import LastIndexed


def get_last_indexed_time() -> int:
    last_indexed_db = list(LastIndexed.select())
    if len(last_indexed_db) < 1:
        last_indexed = LastIndexed.create(last_indexed=0)
    else:
        last_indexed = last_indexed_db[0]

    return int(last_indexed.last_indexed.timestamp())


def set_last_indexed_time(last_indexed_time: int):
    last_indexed = list(LastIndexed.select())[0]
    last_indexed.last_indexed = last_indexed_time
    last_indexed.save()
