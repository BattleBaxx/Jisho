from src.core.db.models.last_indexed import LastIndexed


def get_last_indexed_time() -> int:
    last_indexed_db = list(LastIndexed.select())
    if len(last_indexed_db) < 1:
        return 0

    last_indexed = last_indexed_db[0]
    return int(last_indexed.last_indexed.timestamp())


def set_last_indexed_time(last_indexed_time: int):
    last_indexed_list = list(LastIndexed.select())
    if len(last_indexed_list) == 0:
        LastIndexed.create(last_indexed=last_indexed_time)
    else:
        last_indexed = last_indexed_list[0]
        last_indexed.last_indexed = last_indexed_time
        last_indexed.save()
