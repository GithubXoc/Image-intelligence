import datetime

from server.const import JST_TZ


def get_local_time() -> str:
    return datetime.datetime.now(tz=JST_TZ).isoformat()